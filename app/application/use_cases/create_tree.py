import asyncio
from typing import Callable, Any, Sequence
from uuid import UUID, uuid4
from app.application.event_bus import EventRegistry
from app.application.interfaces import IUnitOfWork
from app.domain import RedBlackTree, TreeNotFoundError


class CreateTreeUseCase:
    """Сценарий создания нового дерева на основе сырых данных."""

    def __init__(self, uow: Callable[[], IUnitOfWork]):
        self._uow = uow

    async def execute(self, raw_data: Sequence[tuple[int, Any]]) -> UUID:
        # Генерация id и пустого дерева
        tree_id = uuid4()
        tree = RedBlackTree(tree_id=tree_id)

        for key, value in raw_data:
            # Вставка одного узла
            tree.insert(key, value)

        # Сохранение заполненного дерева
        async with self._uow() as uow:
            await uow.tree_repo.save(tree)

        return tree_id