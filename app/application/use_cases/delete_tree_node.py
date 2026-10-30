import logging
from typing import Callable
from uuid import UUID
from app.application.event_bus import EventRegistry
from app.application.interfaces import IUnitOfWork
from app.domain import TreeNotFoundError

logger = logging.getLogger()


class DeleteTreeNodeUseCase:
    """Сценарий удаления узла в дереве."""

    def __init__(self, uow: Callable[[], IUnitOfWork], event_register: EventRegistry):
        self._uow = uow
        self._event_register = event_register

    async def execute(self, tree_id: UUID, key: int):
        logger.info('DeleteTreeNodeUseCase: попытка удалить узел key=%s из дерева %s', key, tree_id)

        async with self._uow() as uow:
            # Получить дерево по id
            tree = await uow.tree_repo.get_by_id(tree_id)
            if not tree:
                logger.warning('DeleteTreeNodeUseCase: дерево %s не найдено', tree_id)
                raise TreeNotFoundError(tree_id)

            # Удалить узел и получить доменные события
            tree.delete(key)
            events = tree.domain_event
            tree.clear_events()

            await uow.tree_repo.save(tree)

        # Обработка доменных событий
        for event in events:
            await self._event_register.dispatch(event)

        logger.info('DeleteTreeNodeUseCase: узел key=%s успешно удален из дерева %s', key, tree_id)