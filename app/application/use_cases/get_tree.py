from typing import Callable
from uuid import UUID
from app.application.interfaces import IUnitOfWork


class GetTreeUseCase:
    """Сценарий получения дерева по id."""

    def __init__(self, uow: Callable[[], IUnitOfWork]):
        self._uow = uow

    async def execute(self, tree_id: UUID) -> dict:
        # Получить из хранилища агрегат RedBlackTree
        async with self._uow() as uow:
            tree = await uow.tree_repo.get_by_id(tree_id)
            if not tree:
                raise Exception

        # Маппинг из объекта RedBlackTree -> dict
        return {
            'tree_id': tree.tree_id,
            'size': tree.size,
            'nodes': tree.to_dict()
        }