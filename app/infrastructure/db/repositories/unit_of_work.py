from types import TracebackType
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.repositories.tree_repository import SQLAlchemyTreeRepo
from app.infrastructure.db.session import session_factory
import logging

logger = logging.getLogger()


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
        logger.debug('UoW: открыта новая транзакция')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.warning('UoW: откат транзакции из-за ошибки: %s', exc_val)
            # Если есть ошибка, то откат
            await self.rollback()
        else:
            logger.debug('UoW: коммит транзакции')
            # Если нет, то сохранить
            await self.commit()

        # Закрыть сессию
        await self.session.close()
        logger.debug('UoW: сессия закрыта')

    async def commit(self):
        """Сохранить данные в бд."""
        try:
            await self.session.commit()
        except Exception as e:
            logger.error('UoW: ошибка при коммите транзакции: %s', str(e))
            raise

    async def rollback(self):
        """Откатить все изменения."""
        await self.session.rollback()