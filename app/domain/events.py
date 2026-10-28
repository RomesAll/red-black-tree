from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NodeInsertedEvent:
    """Событие: вставка нового узла."""
    key: Any
    value: Any
    color: str


@dataclass(frozen=True)
class NodeDeletedEvent:
    """Событие: удаление узла."""
    key: Any


@dataclass(frozen=True)
class NodeColorChangedEvent:
    """Событие: смена цвета узла."""
    key: Any
    new_color: str


@dataclass(frozen=True)
class NodeLeftRotatedEvent:
    """Событие: узел повернут влево."""
    key: Any
    new_root_key: Any
    parent_key: Any | None


@dataclass(frozen=True)
class NodeRightRotatedEvent:
    """Событие: узел повернут вправо."""
    key: Any
    new_root_key: Any
    parent_key: Any | None
