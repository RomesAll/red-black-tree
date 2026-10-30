from typing import Callable, Any
from app.application.interfaces import IUnitOfWork
from app.domain import TreeNotFoundError


class DeleteTreeUseCase:
    """Сценарий для полного удаления Агрегата дерева из системы."""

    def __init__(self, uow: Callable[[], IUnitOfWork]):
        self._uow = uow

    async def execute(self, tree_id: Any) -> bool:
        async with self._uow() as uow:
            # Получить агрегат RedBlackTree по id
            tree = await uow.tree_repo.get_by_id(tree_id)
            if tree is None:
                raise TreeNotFoundError(tree_id)

            # Удаление информации о дереве
            await uow.tree_repo.delete(tree_id)
            return True