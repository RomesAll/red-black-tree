import asyncio
from typing import Any
from uuid import UUID
from fastapi import WebSocket


class WebSocketManager:
    """
    Менеджер для управления WebSocket-подключениями.
    """

    def __init__(self):
        # Словарь с tree_id и множеством сокетов, которые подписаны на это дерево.
        self.rooms: dict[UUID, set[WebSocket]] = {}

    async def connect(self, tree_id: UUID, websocket: WebSocket) -> None:
        """Принять новое подключение и добавить клиента в комнату дерева."""
        if tree_id not in self.rooms:
            self.rooms[tree_id] = set()

        self.rooms[tree_id].add(websocket)

    def disconnect(self, tree_id: UUID, websocket: WebSocket) -> None:
        """Удалить клиента из комнаты."""
        if tree_id in self.rooms:
            self.rooms[tree_id].discard(websocket)
            if not self.rooms[tree_id]:
                del self.rooms[tree_id]

    async def send_to_tree(self, tree_id: UUID, payload: dict) -> None:
        """
        Отправить сообщение тем клиентам, которые подписаны на конкретное дерево.
        """
        if tree_id not in self.rooms:
            return

        for connection in list(self.rooms[tree_id]):
            try:
                await connection.send_json(payload)
            except Exception:
                self.disconnect(tree_id, connection)


# Глобальный экземпляр
manager = WebSocketManager()