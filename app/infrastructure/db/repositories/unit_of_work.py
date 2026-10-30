from types import TracebackType
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.repositories.tree_repository import SQLAlchemyTreeRepo
from app.infrastructure.db.session import session_factory


class SQLAlchemyUnitOfWork:
    """
    Реализация паттерна Unit of Work для SQLAlchemy.
    Управляет сессией и транзакциями.
    """

    def __init__(self):
        self._session: AsyncSession | None = None
        self.tree_repo: SQLAlchemyTreeRepo | None = None

    async def __aenter__(self):
        # Создать сессию через фабрику
        self.session = session_factory()

        # Инициализировать репозиторий с передачей сессии
        self.tree_repo = SQLAlchemyTreeRepo(session=self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # Если есть ошибка, то откат
            await self.rollback()
        else:
            # Если нет, то сохранить
            await self.commit()

        # Закрыть сессию
        await self.session.close()

    async def commit(self):
        """Сохранить данные в бд."""
        await self.session.commit()

    async def rollback(self):
        """Откатить все изменения."""
        await self.session.rollback()