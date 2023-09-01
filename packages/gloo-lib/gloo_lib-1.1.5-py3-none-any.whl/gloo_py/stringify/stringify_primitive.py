import typing
from .stringify import StringifyBase

T = typing.TypeVar("T", str, int, float, bool)

class StringifyPrimitive(StringifyBase[T]):
    __type: typing.Type[T]

    def __init__(self, _type: typing.Type[T], args: str) -> None:
        self.__arg = args
        self.__type = _type

    def _json_str(self) -> str:
        return self.__arg

    def parse(self, value: typing.Any) -> T:
        return self.__type(value)

    def vars(self) -> typing.Dict[str, str]:
        return {}

class StringifyNone(StringifyBase[None]):

    def _json_str(self) -> str:
        return 'null'

    def parse(self, value: typing.Any) -> None:
        return None
    
    def vars(self) -> typing.Dict[str, str]:
        return {}

U = typing.TypeVar("U")
class StringifyOptional(StringifyBase[typing.Optional[U]]):
    def __init__(self, args: StringifyBase[U]) -> None:
        self.__args = args

    def _json_str(self) -> str:
        return f'{self.__args.json} | null'
    
    def parse(self, value: typing.Any) -> typing.Optional[U]:
        if value is None:
            return None
        return self.__args.parse(value)

    def vars(self) -> typing.Dict[str, str]:
        return self.__args.vars()
