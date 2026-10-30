import logging
from typing import Callable, Any
from uuid import UUID
from app.application.event_bus import EventRegistry
from app.application.interfaces import IUnitOfWork
from app.domain import TreeNotFoundError

logger = logging.getLogger()


class CreateNodeUseCase:
    """Сценарий создания нового узла в существующем дереве по id."""

    def __init__(self, uow: Callable[[], IUnitOfWork], event_registry: EventRegistry):
        self._uow = uow
        self._event_registry = event_registry

    async def execute(self, tree_id: UUID, key: int, value: Any):
        logger.info('CreateNodeUseCase: попытка вставить узел key=%s в дерево %s', key, tree_id)

        async with self._uow() as uow:
            # Получение дерева из хранилища
            tree = await uow.tree_repo.get_by_id(tree_id)
            if not tree:
                logger.warning('CreateNodeUseCase: дерево %s не найдено', tree_id)
                raise TreeNotFoundError(tree_id)

            # Вставка нового узла
            tree.insert(key, value)

            # Получения доменных событий
            events = tree.domain_event
            tree.clear_events()

            # Сохранение дерева в хранилище
            await uow.tree_repo.save(tree)

        # Обработка доменных событий
        for event in events:
            await self._event_registry.dispatch(event)

        logger.info('CreateNodeUseCase: узел key=%s успешно добавлен в дерево %s', key, tree_id)