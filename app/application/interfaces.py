from typing import Protocol, Any, Self
from uuid import UUID
from app.domain.repository_interfaces import ITreeRepository


class IEventHandler(Protocol):
    """Интерфейс-протокол для одиночного обработчика события."""

    async def handle(self, event: Any) -> None:
        pass


class IWSManager(Protocol):
    """Интерфейс-протокол для отправки данных по вебсокетам."""

    async def send_to_tree(self, tree_id: UUID, payload: dict) -> None:
        pass


class IUseCase(Protocol):
    """Интерфейс-протокол для сценариев использования."""

    async def execute(self, *args, **kwargs) -> Any:
        pass


class IUnitOfWork(Protocol):
    """Интерфейс-протокол для паттерна unit of work."""
    tree_repo: ITreeRepository

    async def __aenter__(self) -> Self:
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass