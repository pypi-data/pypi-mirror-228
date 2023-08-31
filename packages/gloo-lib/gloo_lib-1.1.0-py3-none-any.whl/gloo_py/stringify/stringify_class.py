import typing
from .stringify import StringifyBase, StringifyRemappedField
from ..logging import logger
from pydantic import BaseModel
import json

U = typing.TypeVar("U", bound=BaseModel)
T = typing.TypeVar("T")


class FieldDescription(typing.Generic[T]):
    def __init__(
        self,
        name: str,
        description: None | str,
        type_desc: StringifyBase[T],
    ) -> None:
        self.name = name
        self.__description = description
        self.__type = type_desc

    @property
    def _type(self) -> StringifyBase[T]:
        return self.__type

    @property
    def description(self) -> str:
        if self.__description:
            return self.__description
        return self.__type.json

    def __str__(self) -> str:
        return self.name

    @property
    def json(self) -> str:
        return self.__type.json

    def vars(self) -> typing.Dict[str, str]:
        return self.__type.vars()


def update_field_description(
    field: FieldDescription[T],
    *,
    update: typing.Optional[StringifyRemappedField] = None,
) -> FieldDescription[T]:
    if update is None:
        return field
    return FieldDescription(
        name=update.name or field.name,
        description=update.description or field.description,
        type_desc=field._type,
    )


class StringifyClass(StringifyBase[U]):
    def __init__(
        self,
        *,
        model: typing.Type[U],
        values: typing.Dict[str, FieldDescription[typing.Any]],
        updates: typing.Dict[str, StringifyRemappedField],
    ) -> None:
        props = {
            k: update_field_description(v, update=updates.get(k))
            for k, v in values.items()
        }
        self.__props = props
        self.__reverse_props = {v.name.lower(): k for k, v in props.items()}
        self.__model = model
        self.__name = model.__name__

    def __getattribute__(self, item: str) -> typing.Any:
        # Attempt to return the attribute using the standard method
        try:
            return super().__getattribute__(item)
        except AttributeError:
            # If it fails, use the custom logic in __getattr__
            return self.__getattr__(item)

    def __getattr__(self, item: str) -> FieldDescription[typing.Any]:
        # This will only be called if the attribute is not found through the standard methods
        res = self.__props.get(item)
        if res is None:
            raise AttributeError(f"Unknown field: {item}")
        return res

    def _json_str(self) -> str:
        return json.dumps({v.name: v.description for _, v in self.__props.items()}, indent=2)

    def parse(self, value: typing.Any) -> U:
        if isinstance(value, str):
            value = json.loads(value)
        if not isinstance(value, dict):
            raise ValueError(f"Expected dict, got {value} ({type(value)})")

        # Replace all keys with the renamed keys
        props = self.__props
        rev_props = self.__reverse_props
        value = {
            rev_props[k.lower()]: props[rev_props[k.lower()]]._type.parse(v)
            for k, v in value.items()
            if k.lower() in rev_props
        }
        return self.__model.model_validate(value)

    def vars(self) -> typing.Dict[str, str]:
        v = {
            f"{self.__name}.{k}": {
                "name": v.name,
                "description": v.description,
                'json': v.json,
            }
            for k, v in self.__props.items()
        }
        # Flatten the dict
        x = {
            f"{k}.{k2}": v2
            for k, v in v.items()
            for k2, v2 in v.items()
        }

        for k, v1 in self.__props.items():
            x[f'{self.__name}.{k}'] = v1.name

        x[f"{self.__name}.json"] = self.json
        return x
