import json
import typing
from .stringify import StringifyBase

T = typing.TypeVar("T")
class StringifyList(StringifyBase[typing.List[T]]):
    def __init__(self, args: StringifyBase[T]) -> None:
        self.__args = args

    def _json_str(self) -> str:
        return f"{self.__args.json}[]"
    
    def parse(self, value: typing.Any) -> typing.List[T]:
        if isinstance(value, str):
            if value.startswith("[") and value.endswith("]"):
                value = json.loads(value)
        # Make sure we have a list
        if not isinstance(value, list):
            value = [value]
        return list(map(self.__args.parse, value))

    def vars(self) -> typing.Dict[str, str]:
        return self.__args.vars()
