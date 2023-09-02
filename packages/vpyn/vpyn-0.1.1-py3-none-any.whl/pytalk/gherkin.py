"""Like pickle."""
from types import FunctionType
from collections.abc import Callable
from typing import Type, Optional
from functools import singledispatch

def loads(data: str | bytes) -> object:

    si = SerialInterface()

    if isinstance(obj, list):
        return [copy(i) for i in range(len(obj))]

    pass


def dump_str(data: object) -> str:
    pass


def dump_bytes(data: object) -> bytes:
    pass


def copy(obj: object) -> object:

    cls = type(obj)

    if cls == list:
        return [copy(elt) for elt in obj]

T = Type("T")

class SerialInterfaceProxyObject:
    __type: Optional[type]
    __dict: Optional[dict[str, object]]
    __value: Optional[str | int | byes | bool]
    __iter_items: Optional[...]

    def __call__(self, generator: Callable[[], T]) -> T:
        ...
