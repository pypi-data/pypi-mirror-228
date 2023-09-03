from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from typing import (Any, Callable, Dict, Generic, Iterable, List, Literal,
                    Optional, Type, TypeVar, Union, cast)
from uuid import UUID

from pydantic import BaseConfig  # pylint: disable=no-name-in-module
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import Extra  # pylint: disable=no-name-in-module
from pydantic import Field
from typing_extensions import ParamSpec

from .utils import handle_errors, process_time, setup_logging

Vector = List[float]

MetaData = Dict[str, str]

NoArgAnyCallable = Callable[[], Any]

logger = setup_logging(__name__)

EventTypes = Literal["start", "version", "set", "history_rewrite", "error"]
T = TypeVar("T")
P = ParamSpec("P")


class Document(BaseModel):
    class Config(BaseConfig):
        """Config"""

        extra = Extra.allow
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.astimezone().isoformat(),
            date: lambda v: v.isoformat(),
            time: lambda v: v.isoformat(),
            timedelta: lambda v: v.total_seconds(),
            UUID: lambda v: str(v),
            Decimal: lambda v: float(v),
            "Ref": lambda v: v.id(),
            "FaunaTime": lambda v: v.value,
            Enum: lambda v: v.value,
            Union: lambda v: v.value,
        }

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__doc__ is None:
            cls.__doc__ = f"```json\n{cls.schema_json(indent=2)}\n```"


D = TypeVar("D", bound=Document)


class LazyProxy(Generic[T], ABC):
    def __init__(self) -> None:
        self.__proxied: Union[T, None] = None

    def __getattr__(self, attr: str) -> object:
        return getattr(self.__get_proxied__(), attr)

    def __repr__(self) -> str:
        return repr(self.__get_proxied__())

    def __dir__(self) -> Iterable[str]:
        return self.__get_proxied__().__dir__()

    def __get_proxied__(self) -> T:
        proxied = self.__proxied

        if proxied is not None:
            return proxied

        self.__proxied = proxied = self.__load__()

        return proxied

    def __set_proxied__(self, value: T) -> None:
        self.__proxied = value

    def __as_proxied__(self) -> T:
        """Helper method that returns the current proxy, typed as the loaded object"""

        return cast(T, self)

    @abstractmethod
    def __load__(self) -> T:
        ...

