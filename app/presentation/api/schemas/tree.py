from uuid import UUID
from pydantic import BaseModel, Field
from typing import Any


class TreeCreateRequest(BaseModel):
    """Схема запроса на создание нового дерева."""
    initial_data: list[tuple[int, Any]] = Field(
        default_factory=list,
        description="Список пар (ключ, значение) для начального заполнения"
    )


class NodeResponse(BaseModel):
    """Схема одного узла для ответа клиенту."""
    key: int
    value: Any | None = None
    color: str


class TreeResponse(BaseModel):
    """Схема ответа с полной информацией о дереве."""
    tree_id: UUID
    size: int
    root: dict | None = None