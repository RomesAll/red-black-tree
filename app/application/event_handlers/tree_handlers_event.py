from app.application.interfaces import IWSManager
from app.domain.events import (
    NodeInsertedEvent,
    NodeDeletedEvent,
    NodeColorChangedEvent,
    NodeLeftRotatedEvent,
    NodeRightRotatedEvent
)


class NodeInsertedEventHandler:
    """Обработчик доменного события успешной вставки узла."""

    def __init__(self, ws_manager: IWSManager):
        self.ws_manager = ws_manager

    async def handle(self, event: NodeInsertedEvent) -> None:
        payload = {
            'type': 'NODE_INSERTED',
            'data': {
                'tree_id': str(event.tree_id),
                'key': event.key,
                'value': event.value,
                'color': event.color
            }
        }
        await self.ws_manager.send_to_tree(event.tree_id, payload)


class NodeDeletedEventHandler:
    """Обработчик доменного события удаления узла из дерева."""

    def __init__(self, ws_manager: IWSManager):
        self.ws_manager = ws_manager

    async def handle(self, event: NodeDeletedEvent) -> None:
        payload = {
            'type': 'NODE_DELETED',
            'data': {
                'tree_id': str(event.tree_id),
                'key': event.key
            }
        }
        await self.ws_manager.send_to_tree(event.tree_id, payload)


class NodeColorChangedEventHandler:
    """Обработчик доменного события изменения цвета узла при балансировке."""

    def __init__(self, ws_manager: IWSManager):
        self.ws_manager = ws_manager

    async def handle(self, event: NodeColorChangedEvent) -> None:
        payload = {
            'type': 'COLOR_CHANGED',
            'data': {
                'tree_id': str(event.tree_id),
                'key': event.key,
                'new_color': event.new_color
            }
        }
        await self.ws_manager.send_to_tree(event.tree_id, payload)


class NodeLeftRotatedEventHandler:
    """Обработчик доменного события левого поворота поддерева."""

    def __init__(self, ws_manager: IWSManager):
        self.ws_manager = ws_manager

    async def handle(self, event: NodeLeftRotatedEvent) -> None:
        payload = {
            'type': 'ROTATE_LEFT',
            'data': {
                'tree_id': str(event.tree_id),
                'key': event.key,
                'new_root_key': event.new_root_key,
                'parent_key': event.parent_key
            }
        }
        await self.ws_manager.send_to_tree(event.tree_id, payload)


class NodeRightRotatedEventHandler:
    """Обработчик доменного события правого поворота поддерева."""

    def __init__(self, ws_manager: IWSManager):
        self.ws_manager = ws_manager

    async def handle(self, event: NodeRightRotatedEvent) -> None:
        payload = {
            'type': 'ROTATE_RIGHT',
            'data': {
                'tree_id': str(event.tree_id),
                'key': event.key,
                'new_root_key': event.new_root_key,
                'parent_key': event.parent_key
            }
        }
        await self.ws_manager.send_to_tree(event.tree_id, payload)
