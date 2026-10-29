from typing import Type, Any
from app.application.interfaces import IEventHandler


class EventRegistry:
    """Реестр доменных событий (Event Bus)."""

    def __init__(self):
        self._handlers: dict[Type[Any], IEventHandler] = {}

    def register(self, event_type: Type[Any], handler: IEventHandler) -> None:
        """Метод для наполнения реестра при старте приложения."""
        self._handlers[event_type] = handler

    async def dispatch(self, event: Any) -> None:
        """Обработка доменных событий"""
        event_type = type(event)
        handler = self._handlers.get(event_type)

        if handler:
            await handler.handle(event)
