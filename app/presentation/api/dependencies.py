from app.application.interfaces import IUnitOfWork, IEventHandler
from app.infrastructure.db import SQLAlchemyUnitOfWork
from app.application.event_bus import EventRegistry


event_bus = EventRegistry()


def get_uow() -> IUnitOfWork:
    """Создать Unit of Work для каждого HTTP-запроса."""
    return SQLAlchemyUnitOfWork


def get_event_bus() -> EventRegistry:
    """Получить Event Bus."""
    return event_bus