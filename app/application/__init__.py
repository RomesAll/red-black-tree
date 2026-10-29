# Метаданные пакета
__author__ = "RomesAll"
__version__ = "0.1.0"

# Обработчики доменных событий
from .event_handlers import (
    NodeRightRotatedEventHandler,
    NodeLeftRotatedEventHandler,
    NodeInsertedEventHandler,
    NodeDeletedEventHandler,
    NodeColorChangedEventHandler,
)

# Сценарии использования
from .use_cases import (
    StreamCreateTreeUseCase,
    GetTreeUseCase,
    DeleteTreeNodeUseCase,
    DeleteTreeUseCase,
    CreateNodeUseCase,
    CreateTreeUseCase
)

# Реестр событий
from .event_bus import EventRegistry

# Интерфейсы
from .interfaces import (
    IUnitOfWork,
    IEventHandler,
    IUseCase,
    IWSManager,
    ITreeRepository
)


__all__ = [
    # Обработчики
    'NodeRightRotatedEventHandler',
    'NodeLeftRotatedEventHandler',
    'NodeInsertedEventHandler',
    'NodeDeletedEventHandler',
    'NodeColorChangedEventHandler',
    # Сценарии
    'StreamCreateTreeUseCase',
    'GetTreeUseCase',
    'DeleteTreeNodeUseCase',
    'DeleteTreeUseCase',
    'CreateNodeUseCase',
    'CreateTreeUseCase',
    # Реестр событий,
    'EventRegistry',
    # Интерфейсы
    'IUnitOfWork',
    'IEventHandler',
    'IUseCase',
    'IWSManager',
    'ITreeRepository'
]