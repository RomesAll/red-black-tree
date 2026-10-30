# API
from fastapi import FastAPI
from .nodes import router as nodes_router
from .trees import router as trees_router
from .ws_routes import router as ws_router


def register_api(app: FastAPI):
    """Регистрация api endpoints"""
    app.include_router(nodes_router)
    app.include_router(trees_router)
    app.include_router(ws_router)


__all__ = [
    'register_api'
]