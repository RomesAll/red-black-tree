from pydantic import BaseModel
from typing import Any


class NodeCreateRequest(BaseModel):
    """Схема запроса на добавление узла в дерево."""
    key: int
    value: Any | None = None


class NodeDeleteRequest(BaseModel):
    """Схема запроса на удаление узла из дерева."""
    key: int