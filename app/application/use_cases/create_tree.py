import asyncio
import logging
from typing import Callable, Any, Sequence
from uuid import UUID, uuid4
from app.application.event_bus import EventRegistry
from app.application.interfaces import IUnitOfWork
from app.domain import RedBlackTree, TreeNotFoundError

logger = logging.getLogger()


class CreateTreeUseCase:
    """Сценарий создания нового дерева на основе сырых данных."""

    def __init__(self, uow: Callable[[], IUnitOfWork]):
        self._uow = uow

    async def execute(self, raw_data: Sequence[tuple[int, Any]]) -> UUID:
        # Генерация id и пустого дерева
        tree_id = uuid4()
        tree = RedBlackTree(tree_id=tree_id)

        logger.info('CreateTreeUseCase: создание дерева %s с %d узлами', tree_id, len(raw_data))

        for key, value in raw_data:
            # Вставка одного узла
            tree.insert(key, value)

        # Сохранение заполненного дерева
        async with self._uow() as uow:
            await uow.tree_repo.save(tree)

        logger.info('CreateTreeUseCase: дерево %s успешно сохранено', tree_id)
        return tree_id