from typing import Callable, Any
from app.application.interfaces import IUnitOfWork


class DeleteTreeUseCase:
    """Сценарий для полного удаления Агрегата дерева из системы."""

    def __init__(self, uow_factory: Callable[[], IUnitOfWork]):
        self._uow_factory = uow_factory

    async def execute(self, tree_id: Any) -> bool:
        async with self._uow_factory() as uow:
            # Получить агрегат RedBlackTree по id
            tree = await uow.tree_repo.get_by_id(tree_id)
            if tree is None:
                return False

            # Удаление информации о дереве
            await uow.tree_repo.delete(tree_id)
            return True