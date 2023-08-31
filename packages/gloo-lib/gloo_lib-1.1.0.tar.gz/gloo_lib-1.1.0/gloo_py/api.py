from datetime import datetime
import typing
import aiohttp
from .api_types import IO, EventChain, LogSchema, LogSchemaContext, Error, MetadataType
from .env import ENV
from .logging import logger
from .common import event_chain_var, event_tags_var, event_metadata_var
import requests


class APIWrapper:
    def __init__(self) -> None:
        self.base_url = ENV.GLOO_BASE_URL
        key = ENV.GLOO_APP_SECRET

        self.headers = {
            "Content-Type": "application/json",
        }
        if key:
            self.headers["Authorization"] = f"Bearer {key}"

    async def _call_api(self, endpoint: str, payload: LogSchema) -> typing.Any:
        async with aiohttp.ClientSession() as session:
            data = payload.model_dump(by_alias=True)
            print(data)
            async with session.post(
                f"{self.base_url}/{endpoint}", headers=self.headers, json=data
            ) as response:
                if response.status != 200:
                    text = await response.text()
                    raise Exception(
                        f"Failed with status code {response.status}: {text}"
                    )

                return await response.json()

    def _call_api_sync(self, endpoint: str, payload: LogSchema) -> typing.Any:
        with requests.Session() as session:
            data = payload.model_dump(by_alias=True)
            print(data)
            response = session.post(
                f"{self.base_url}/{endpoint}", headers=self.headers, json=data
            )
            if response.status_code != 200:
                raise Exception(
                    f"Failed with status code {response.status_code}: {response.text}"
                )

            return response.json()

    def _prepare_log_payload(
        self,
        *,
        event_type: typing.Literal["log", "func_llm", "func_prob", "func_code"],
        io: IO,
        error: typing.Optional[Error] = None,
    ) -> LogSchema | None:
        tags_chain = event_tags_var.get()
        event_chain = event_chain_var.get()
        metadata_dict = event_metadata_var.get()
        tags = tags_chain[-1] if tags_chain else None

        if not event_chain:
            logger.warning("Attempted to log outside of an event chain.")
            return

        root_event = event_chain[0]
        last_event = event_chain[-1]

        metadata_key = f"{last_event.func_name}"
        if last_event.variant_name:
            metadata_key = f"{metadata_key}::{last_event.variant_name}"
        metadata = metadata_dict.pop(metadata_key, None) if metadata_dict else None

        now = datetime.utcnow()
        context = LogSchemaContext(
            start_time=last_event.timestamp.isoformat() + "Z",
            hostname=ENV.HOSTNAME,
            process_id=ENV.GLOO_PROCESS_ID,
            stage=ENV.GLOO_STAGE,
            latency_ms=int((now - last_event.timestamp).total_seconds() * 1000),
            tags=tags if tags else {},
            event_chain=list(
                map(
                    lambda x: EventChain(
                        function_name=x.func_name,
                        variant_name=x.variant_name,
                    ),
                    event_chain,
                )
            ),
        )
        payload = LogSchema(
            project_id=ENV.GLOO_APP_ID,
            event_type=event_type,
            event_id=last_event.event_id,
            root_event_id=root_event.event_id,
            context=context,
            error=error,
            metadata=metadata,
            io=io,
        )
        return payload

    def log_sync(
        self,
        *,
        event_type: typing.Literal["log", "func_llm", "func_prob", "func_code"],
        io: IO,
        error: typing.Optional[Error] = None,
    ) -> None:
        payload = self._prepare_log_payload(event_type=event_type, io=io, error=error)
        if payload is None:
            return
        try:
            self._call_api_sync("log/v2", payload)
        except Exception as e:
            event_name = payload.context.event_chain[-1].function_name
            if payload.context.event_chain[-1].variant_name:
                event_name = (
                    f"{event_name}::{payload.context.event_chain[-1].variant_name}"
                )
            logger.warning(f"Log failure on {event_name}: {e}")
            logger.debug(f"Dropped Payload: {payload}")

    async def log(
        self,
        *,
        event_type: typing.Literal["log", "func_llm", "func_prob", "func_code"],
        io: IO,
        error: typing.Optional[Error] = None,
    ) -> None:
        payload = self._prepare_log_payload(event_type=event_type, io=io, error=error)
        if payload is None:
            return
        try:
            await self._call_api("log/v2", payload)
        except Exception as e:
            event_name = payload.context.event_chain[-1].function_name
            if payload.context.event_chain[-1].variant_name:
                event_name = (
                    f"{event_name}::{payload.context.event_chain[-1].variant_name}"
                )
            logger.warning(f"Log failure on {event_name}: {e}")
            logger.debug(f"Dropped Payload: {payload}")
