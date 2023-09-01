from contextvars import ContextVar
from datetime import datetime
import typing
import uuid
from .api_types import MetadataType


# Define the named tuple 'Event'
class EventBase:
    func_name: str
    variant_name: str | None
    timestamp: datetime

    def __init__(self, *, func_name: str, variant_name: str | None):
        self.func_name = func_name
        self.variant_name = variant_name
        self.event_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()


# Initialize the context variable 'event_chain_var'
event_chain_var: ContextVar[typing.Optional[typing.List[EventBase]]] = ContextVar(
    "event_chain", default=None
)
event_tags_var: ContextVar[
    typing.Optional[typing.List[typing.Dict[str, str]]]
] = ContextVar("event_tags", default=None)
event_metadata_var: ContextVar[
    typing.Optional[typing.Dict[str, MetadataType]]
] = ContextVar("event_metadata", default=None)


def set_eventmetadata(metadata: MetadataType, *, event_name: None | str = None) -> None:
    if event_name is None:
        chain = event_chain_var.get()
        if not chain:
            raise ValueError("event_name must be specified if event_chain is not set")
        last_event = chain[-1]
        event_name = last_event.func_name
        if last_event.variant_name:
            event_name += "::" + last_event.variant_name
    meta = event_metadata_var.get()
    if meta is None:
        event_metadata_var.set({event_name: metadata})
    else:
        meta[event_name] = metadata
