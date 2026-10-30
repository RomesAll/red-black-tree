from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class NodeInsertedEvent:
    """Событие: вставка нового узла."""
    tree_id: UUID
    key: Any
    value: Any
    color: str


@dataclass(frozen=True)
class NodeDeletedEvent:
    """Событие: удаление узла."""
    tree_id: UUID
    key: Any


@dataclass(frozen=True)
class NodeColorChangedEvent:
    """Событие: смена цвета узла."""
    tree_id: UUID
    key: Any
    new_color: str


@dataclass(frozen=True)
class NodeLeftRotatedEvent:
    """Событие: узел повернут влево."""
    tree_id: UUID
    key: Any
    new_root_key: Any
    parent_key: Any | None


@dataclass(frozen=True)
class NodeRightRotatedEvent:
    """Событие: узел повернут вправо."""
    tree_id: UUID
    key: Any
    new_root_key: Any
    parent_key: Any | None
