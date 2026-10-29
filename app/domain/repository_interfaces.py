from typing import Any, Protocol
from app.domain.models.rbt_tree import RedBlackTree


class ITreeRepository(Protocol):
    """
    Интерфейс-протокол репозитория для управления агрегатом RedBlackTree
    """

    async def get_by_id(self, tree_id: Any) -> RedBlackTree | None:
        """Получить агрегата по id"""
        pass

    async def save(self, tree: RedBlackTree) -> None:
        """Сохранить новый агрегат по id"""
        pass

    async def delete(self, tree_id: Any) -> None:
        """Удалить агрегат по id"""
        pass
