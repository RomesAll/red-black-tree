import logging
from typing import Callable
from uuid import UUID
from app.application.interfaces import IUnitOfWork
from app.domain import TreeNotFoundError

logger = logging.getLogger()


class GetTreeUseCase:
    """Сценарий получения дерева по id."""

    def __init__(self, uow: Callable[[], IUnitOfWork]):
        self._uow = uow

    async def execute(self, tree_id: UUID) -> dict:
        logger.info('GetTreeUseCase: запрос дерева %s', tree_id)

        # Получить из хранилища агрегат RedBlackTree
        async with self._uow() as uow:
            tree = await uow.tree_repo.get_by_id(tree_id)
            if not tree:
                logger.warning('GetTreeUseCase: дерево %s не найдено', tree_id)
                raise TreeNotFoundError(tree_id)

        return {
            'tree_id': tree.tree_id,
            'size': tree.size,
            'root': tree.to_dict()
        }