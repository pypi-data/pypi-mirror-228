import abc
import typing

T = typing.TypeVar("T")
class StringifyBase(abc.ABC, typing.Generic[T]):
    @property
    def json(self) -> str:
        return self._json_str()
    
    @abc.abstractmethod
    def _json_str(self) -> str:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def parse(self, value: typing.Any) -> T:
        raise NotImplementedError()

    @abc.abstractmethod
    def vars(self) -> typing.Dict[str, str]:
        raise NotImplementedError()

class StringifyRemappedField:
    def __init__(self, *, rename: typing.Optional[str] = None, describe: typing.Optional[str] = None, skip: bool = False) -> None:
        self.name = rename
        self.description = describe
        self.skip = skip
