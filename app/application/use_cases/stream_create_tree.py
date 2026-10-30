import asyncio
import logging
from typing import Callable, Any, Sequence, Awaitable
from uuid import UUID, uuid4
from app.application.event_bus import EventRegistry
from app.application.interfaces import IUnitOfWork
from app.domain import RedBlackTree

logger = logging.getLogger()


class StreamCreateTreeUseCase:
    """Сценарий создания нового дерева на основе сырых данных с real-time стримингом."""

    def __init__(self, uow: Callable[[], IUnitOfWork], event_registry: EventRegistry):
        self._uow = uow
        self._event_registry = event_registry

    async def execute(
            self,
            tree_id: UUID,
            raw_data: Sequence[tuple[int, Any]],
            delay: float = 0.3,
    ) -> UUID:
        tree = RedBlackTree(tree_id=tree_id)
        logger.info('StreamCreateTreeUseCase: старт стриминга для дерева %s. Узлов: %d', tree_id, len(raw_data))

        for key, value in raw_data:
            # Вставка одного узла
            tree.insert(key, value)

            # Получение и очистка доменных событий
            events = tree.domain_event
            tree.domain_event.clear()

            # Сохранить дерево в хранилище
            async with self._uow() as uow:
                await uow.tree_repo.save(tree)

            # Обработка доменных событий
            for event in events:
                await self._event_registry.dispatch(event)

            await asyncio.sleep(delay)

        logger.info('StreamCreateTreeUseCase: стриминг успешно завершен для дерева %s', tree_id)
        return tree_id