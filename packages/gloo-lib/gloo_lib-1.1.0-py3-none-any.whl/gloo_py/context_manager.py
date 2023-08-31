import abc
import contextlib
from datetime import datetime
import traceback
from types import TracebackType
import typing
from .common import EventBase, event_chain_var, event_metadata_var, event_tags_var
from .env import ENV
from .api import APIWrapper
from .api_types import (
    IO,
    IOValue,
    TypeSchema,
    Error,
    LLMEventSchema,
    LLMEventInput,
    LLMEventInputPrompt,
)
from .llm_client import LLMClient
from .logging import logger

InputType = typing.TypeVar("InputType")
OutputType = typing.TypeVar("OutputType")

T = typing.TypeVar("T")


def validate_instance(input: typing.Any, type: typing.Type[T]) -> bool:
    origin = typing.get_origin(type)
    args = typing.get_args(type)

    # If no origin, it's a plain type
    if origin is None:
        return isinstance(input, type)

    # Check Union types
    if origin == typing.Union:
        return any(validate_instance(input, alt_type) for alt_type in args)

    # Check List types
    if origin == typing.List:
        if not isinstance(input, list):
            return False
        item_type = args[0]
        return all(validate_instance(item, item_type) for item in input)

    # Check Dict types
    if origin == typing.Dict:
        if not isinstance(input, dict):
            return False
        key_type, value_type = args
        return all(
            validate_instance(k, key_type) and validate_instance(v, value_type)
            for k, v in input.items()
        )

    # Check Set types
    if origin == typing.Set:
        if not isinstance(input, set):
            return False
        item_type = args[0]
        return all(validate_instance(item, item_type) for item in input)

    # If we reach here, the type wasn't one we explicitly handle
    return False


class GlooLoggerCtx:
    __event_type: typing.Literal["log"]

    def __init__(
        self,
        *,
        scope_name: str,
    ):
        self.__api = APIWrapper()
        self.__event_type = "log"
        self.__event_name = scope_name

    async def log(self, *, val: typing.Any) -> None:
        await self.__api.log(
            event_type="log",
            io=IO(
                input=None,
                output=IOValue(
                    value=val, type=TypeSchema(name=type(val).__name__, fields={})
                ),
            ),
            error=None,
        )

    def log_sync(self, *, val: typing.Any) -> None:
        self.__api.log_sync(
            event_type="log",
            io=IO(
                input=None,
                output=IOValue(
                    value=val, type=TypeSchema(name=str(type(val).__name__), fields={})
                ),
            ),
            error=None,
        )

    def __enter__(self) -> "GlooLoggerCtx":
        event_chain = event_chain_var.get()
        if event_chain is None:
            event_chain = [EventBase(func_name=self.__event_name, variant_name=None)]
            event_chain_var.set(event_chain)
        else:
            # If the event_chain already exists, append to it
            event_chain.append(
                EventBase(func_name=self.__event_name, variant_name=None)
            )
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        tb: typing.Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            formatted_traceback = "".join(
                traceback.format_exception(exc_type, exc_value, tb)
            )
            error = Error(
                # TODO: For GlooErrors, we should have a list of error codes.
                code=1,  # Unknown error.
                message=f"{exc_type.__name__}: {exc_value}",
                traceback=formatted_traceback,
            )
            self.__api.log_sync(
                event_type=self.__event_type,
                io=IO(input=None, output=None),
                error=error,
            )
        else:
            error = None

        # Pop off the most recent event
        event_chain = event_chain_var.get()
        if event_chain:
            event_chain.pop()

        # If the event_chain is empty after the pop, set the context variable back to None
        if not event_chain:
            event_chain_var.set(None)

        if error:
            raise Exception(error)

    async def __aenter__(self) -> "GlooLoggerCtx":
        event_chain = event_chain_var.get()
        if event_chain is None:
            event_chain = [EventBase(func_name=self.__event_name, variant_name=None)]
            event_chain_var.set(event_chain)
        else:
            # If the event_chain already exists, append to it
            event_chain.append(
                EventBase(func_name=self.__event_name, variant_name=None)
            )
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        tb: typing.Optional[TracebackType],
    ) -> typing.Optional[bool]:
        if exc_type is not None:
            formatted_traceback = "".join(
                traceback.format_exception(exc_type, exc_value, tb)
            )
            error = Error(
                # TODO: For GlooErrors, we should have a list of error codes.
                code=1,  # Unknown error.
                message=f"{exc_type.__name__}: {exc_value}",
                traceback=formatted_traceback,
            )
        else:
            error = None

        await self.__api.log(
            event_type=self.__event_type, io=IO(input=None, output=None), error=error
        )

        # Pop off the most recent event
        event_chain = event_chain_var.get()
        if event_chain:
            event_chain.pop()

        # If the event_chain is empty after the pop, set the context variable back to None
        if not event_chain:
            event_chain_var.set(None)

        # TODO: Determine if we should return True or None here.
        # If we return True, the exception is suppressed in all parent context managers.
        return error is None


class GlooTagsCtx:
    def __init__(self, **kwargs: str) -> None:
        self.__tags = kwargs
        # Convert all values to strings
        for key, value in self.__tags.items():
            if not isinstance(value, str):
                as_str = str(value)
                truncated = as_str[:10] + "..." if len(as_str) > 10 else as_str
                logger.warning(
                    f"Tag {key}={value} is {type(value)}. Using as string: {truncated}"
                )
                self.__tags[key] = as_str

    def _set_ctx(self) -> None:
        tags_chain = event_tags_var.get()
        if tags_chain is None:
            tags_chain = [self.__tags]
            event_tags_var.set(tags_chain)
        else:
            prev_tags = tags_chain[-1] or {}
            prev_tags_copy = prev_tags.copy()
            prev_tags_copy.update(self.__tags)
            tags_chain.append(prev_tags_copy)

    def _unset_ctx(self) -> None:
        tags_chain = event_tags_var.get()
        if tags_chain:
            tags_chain.pop()
        if not tags_chain:
            event_tags_var.set(None)

    async def __aenter__(self) -> None:
        self._set_ctx()

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        tb: typing.Optional[TracebackType],
    ) -> None:
        self._unset_ctx()

    def __enter__(self) -> None:
        self._set_ctx()

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        tb: typing.Optional[TracebackType],
    ) -> None:
        self._unset_ctx()


class GlooCtx(typing.Generic[InputType, OutputType]):
    __event_type: typing.Literal["func_llm", "func_prob", "func_code"]

    def __init__(
        self,
        *,
        function: str,
        variant: str,
        event_type: typing.Literal["func_llm", "func_prob", "func_code"],
        arg: InputType,
    ):
        self.__function = function
        self.__variant = variant
        self.__io = IO(
            input=IOValue(
                value=arg, type=TypeSchema(name=type(arg).__name__, fields={})
            ),
            output=None,
        )
        self.__api = APIWrapper()
        self.__event_type = event_type

    def set_result(self, result: OutputType) -> None:
        self.__io.output = IOValue(
            value=result, type=TypeSchema(name=type(result).__name__, fields={})
        )

    async def __aenter__(self) -> "GlooCtx[InputType, OutputType]":
        event_chain = event_chain_var.get()
        if event_chain is None:
            event_chain = [
                EventBase(func_name=self.__function, variant_name=self.__variant)
            ]
            event_chain_var.set(event_chain)
        else:
            # If the event_chain already exists, append to it
            event_chain.append(
                EventBase(func_name=self.__function, variant_name=self.__variant)
            )
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        tb: typing.Optional[TracebackType],
    ) -> typing.Optional[bool]:
        if exc_type is not None:
            formatted_traceback = "".join(
                traceback.format_exception(exc_type, exc_value, tb)
            )
            error = Error(
                # TODO: For GlooErrors, we should have a list of error codes.
                code=1,  # Unknown error.
                message=f"{exc_type.__name__}: {exc_value}",
                traceback=formatted_traceback,
            )
        else:
            error = None

        await self.__api.log(event_type=self.__event_type, io=self.__io, error=error)

        # Pop off the most recent event
        event_chain = event_chain_var.get()
        if event_chain:
            event_chain.pop()

        # If the event_chain is empty after the pop, set the context variable back to None
        if not event_chain:
            event_chain_var.set(None)

        # TODO: Determine if we should return True or None here.
        # If we return True, the exception is suppressed in all parent context managers.
        return error is None


def chained(
    func: typing.Callable[
        ["GlooVariant[InputType, OutputType]", InputType], typing.Awaitable[OutputType]
    ]
) -> typing.Callable[..., typing.Awaitable[OutputType]]:
    async def wrapper(
        self: "GlooVariant[InputType, OutputType]", arg: InputType
    ) -> OutputType:
        async with GlooCtx[InputType, OutputType](
            function=self.func_name,
            variant=self.name,
            arg=arg,
            event_type=self.variant_type,
        ) as ctx:
            res = await func(self, arg)
            ctx.set_result(res)
        return res

    return wrapper


class GlooVariant(typing.Generic[InputType, OutputType]):
    __func_name: str
    __name: str

    def __init__(self, *, func_name: str, name: str):
        self.__func_name = func_name
        self.__name = name

    @property
    def variant_type(self) -> typing.Literal["func_llm", "func_prob", "func_code"]:
        if isinstance(self, CodeVariant):
            return "func_code"
        elif isinstance(self, LLMVariant):
            return "func_llm"
        else:
            raise NotImplementedError("Unknown variant type.")

    @property
    def name(self) -> str:
        return self.__name

    @property
    def func_name(self) -> str:
        return self.__func_name

    @abc.abstractmethod
    async def _run(self, arg: InputType) -> OutputType:
        raise NotImplementedError

    @chained
    async def run(self, arg: InputType) -> OutputType:
        response = await self._run(arg)
        # assert validate_instance(
        #     response, OutputType
        # ), f"Response type {type(response)} does not match expected type {OutputType}"
        return response


class CodeVariant(GlooVariant[InputType, OutputType]):
    __func: typing.Callable[[InputType], typing.Awaitable[OutputType]]

    def __init__(
        self,
        func_name: str,
        name: str,
        *,
        func: typing.Callable[[InputType], typing.Awaitable[OutputType]],
    ):
        super().__init__(func_name=func_name, name=name)
        self.__func = func

    async def _run(self, arg: InputType) -> OutputType:
        return await self.__func(arg)


class LLMVariant(GlooVariant[InputType, OutputType]):
    __prompt: str
    __client: LLMClient

    def __init__(
        self,
        func_name: str,
        name: str,
        *,
        prompt: str,
        client: LLMClient,
        prompt_vars: typing.Callable[
            [InputType], typing.Awaitable[typing.Dict[str, str]]
        ],
        parser: typing.Callable[[str], typing.Awaitable[OutputType]],
    ):
        super().__init__(func_name=func_name, name=name)
        self.__prompt = prompt
        self.__client = client
        self.__prompt_vars = prompt_vars
        self.__parser = parser

    async def _run(self, arg: InputType) -> OutputType:
        prompt_vars = await self.__prompt_vars(arg)

        # Determine which prompt vars are used in the prompt string.
        # format is {@var_name}
        used_vars = set()
        for var_name in prompt_vars:
            if f"{{@{var_name}}}" in self.__prompt:
                used_vars.add(var_name)

        # If there are unused vars, log a warning
        unused_vars = set(prompt_vars.keys()) - used_vars
        if unused_vars:
            logger.warning(f"Unused prompt vars\n: {unused_vars}")

        prompt_vars_copy = {var_name: prompt_vars[var_name] for var_name in used_vars}

        response = await self.__client.run(self.__prompt, vars=prompt_vars_copy)
        return await self.__parser(response)
