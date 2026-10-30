import logging
from typing import Callable, Any
from app.application.interfaces import IUnitOfWork
from app.domain import TreeNotFoundError

logger = logging.getLogger()


class DeleteTreeUseCase:
    """Сценарий для полного удаления Агрегата дерева из системы."""

    def __init__(self, uow: Callable[[], IUnitOfWork]):
        self._uow = uow

    async def execute(self, tree_id: Any) -> bool:
        logger.info('DeleteTreeUseCase: попытка удалить дерево %s', tree_id)

        async with self._uow() as uow:
            # Получить агрегат RedBlackTree по id
            tree = await uow.tree_repo.get_by_id(tree_id)
            if tree is None:
                logger.warning('DeleteTreeUseCase: дерево %s не найдено', tree_id)
                raise TreeNotFoundError(tree_id)

            # Удаление информации о дереве
            await uow.tree_repo.delete(tree_id)

        logger.info('DeleteTreeUseCase: дерево %s успешно удалено', tree_id)
        return True