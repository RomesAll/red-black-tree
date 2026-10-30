from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.infrastructure.db.session import init_db, engine
from app.presentation.api.dependencies import get_event_bus
from app.presentation.api.websockets.connection_manager import manager
from app.domain.events import (
    NodeInsertedEvent,
    NodeDeletedEvent,
    NodeColorChangedEvent,
    NodeLeftRotatedEvent,
    NodeRightRotatedEvent
)
from app.application import (
    NodeInsertedEventHandler,
    NodeDeletedEventHandler,
    NodeColorChangedEventHandler,
    NodeLeftRotatedEventHandler,
    NodeRightRotatedEventHandler
)
from app.domain.exceptions import DomainError, TreeNotFoundError, DuplicateKeyError
from app.presentation.api.routers import register_api
from app.presentation.web.router import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация бд
    await init_db()

    # Регистрация доменный событий
    event_bus = get_event_bus()
    event_bus.register(NodeInsertedEvent, NodeInsertedEventHandler(manager))
    event_bus.register(NodeDeletedEvent, NodeDeletedEventHandler(manager))
    event_bus.register(NodeColorChangedEvent, NodeColorChangedEventHandler(manager))
    event_bus.register(NodeLeftRotatedEvent, NodeLeftRotatedEventHandler(manager))
    event_bus.register(NodeRightRotatedEvent, NodeRightRotatedEventHandler(manager))

    yield

    # Закрыть соединение с бд
    await engine.dispose()


app = FastAPI(
    title="Red-Black Tree API",
    description="API для управления красно-черными деревьями",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрация api
app.mount("/static", StaticFiles(directory="app/presentation/web/static"), name="static")
app.include_router(web_router)
register_api(app)


@app.exception_handler(TreeNotFoundError)
async def tree_not_found_handler(request: Request, exc: TreeNotFoundError):
    """Если дерево не найдено — возвращаем 404."""
    return JSONResponse(
        status_code=404,
        content={"error": "Объект не найден", "message": str(exc)}
    )


@app.exception_handler(DuplicateKeyError)
async def duplicate_key_handler(request: Request, exc: DuplicateKeyError):
    """Если ключ уже существует — возвращаем 409 Conflict."""
    return JSONResponse(
        status_code=409,
        content={"error": "Ключ для дерева уже существует", "message": str(exc)}
    )


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    """Любая другая доменная ошибка — возвращаем 400."""
    return JSONResponse(
        status_code=400,
        content={"error": "Ошибка запроса", "message": str(exc)}
    )