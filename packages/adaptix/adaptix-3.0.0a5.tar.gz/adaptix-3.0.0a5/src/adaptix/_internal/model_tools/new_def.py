from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Any, FrozenSet, Optional, Callable, TypeVar, Generic, Union

from adaptix import TypeHint
from adaptix._internal.common import VarTuple
from adaptix._internal.utils import SingletonMeta

T = TypeVar('T')


class NoDefault(metaclass=SingletonMeta):
    pass


@dataclass(frozen=True)
class DefaultValue(Generic[T]):
    value: T

    def __hash__(self):
        try:
            return hash(self.value)
        except TypeError:
            return 236  # some random number that fits in byte


@dataclass(frozen=True)
class DefaultFactory(Generic[T]):
    factory: Callable[[], T]


Default = Union[NoDefault, DefaultValue[T], DefaultFactory[T]]


@dataclass(frozen=True)
class ParamKwargs:
    type: TypeHint


class ParamKind(Enum):
    POS_ONLY = 0
    POS_OR_KW = 1
    KW_ONLY = 3  # 2 is for VAR_POS


@dataclass(frozen=True)
class Parameter:
    field_id: str
    name: str
    kind: ParamKind
    is_required: bool


@dataclass(frozen=True)
class InputShape:
    params: VarTuple[Parameter]
    kwargs: Optional[ParamKwargs]
    constructor: Callable[..., Any]


@dataclass(frozen=True)
class Field:
    id: str
    type: TypeHint
    default: Default
    # Mapping almost never defines __hash__,
    # so it will be more convenient to exclude this field
    # from hash computation
    metadata: Mapping[Any, Any] = field(hash=False)
    original: Any = field(hash=False)


@dataclass(frozen=True)
class Shape:
    fields: VarTuple[Field]
    overriden_types: FrozenSet[str]
