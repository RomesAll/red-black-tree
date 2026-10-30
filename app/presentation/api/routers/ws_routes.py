from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.application import StreamCreateTreeUseCase, CreateTreeUseCase, IUnitOfWork, EventRegistry
from app.infrastructure import SQLAlchemyUnitOfWork
from app.presentation.api.websockets.connection_manager import manager
from app.presentation.api.dependencies import get_event_bus
import logging

router = APIRouter()
logger = logging.getLogger()


@router.websocket('/ws/trees/stream')
async def websocket_tree_create_stream(
    websocket: WebSocket,
    event_bus: EventRegistry = Depends(get_event_bus)
):
    """Подписка и создание в режиме real-time нового дерева."""
    await websocket.accept()
    tree_id: UUID | None = None

    try:
        # Получить данные для дерева
        client_data = await websocket.receive_json()
        raw_data = client_data.get('nodes', [])
        tree_id_str = client_data.get('tree_id')

        if not raw_data or not tree_id_str:
            logger.warning('WebSocket стриминг: клиент не передал данные или tree_id')
            await websocket.send_json({'message': 'Нет данных или ID дерева'})
            return

        tree_id = UUID(tree_id_str)
        logger.info('WebSocket стриминг: старт для дерева %s, узлов: %d', tree_id, len(raw_data))

        # Подписать ws на события дерева
        await manager.connect(tree_id, websocket)
        await websocket.send_json({"status": "Старт", "tree_id": str(tree_id)})

        # Запустить стриминг создания дерева
        await StreamCreateTreeUseCase(
            uow=SQLAlchemyUnitOfWork,
            event_registry=event_bus
        ).execute(
            tree_id=tree_id,
            raw_data=raw_data,
            delay=0.5
        )

        logger.info('WebSocket стриминг: успешно завершен для дерева %s', tree_id)
        await websocket.send_json({"status": "Конец", "tree_id": str(tree_id)})

    except WebSocketDisconnect:
        logger.warning('Клиент отключился от стриминга дерева %s', tree_id)

    except Exception:
        logger.exception('Ошибка в WebSocket стриминге для дерева %s', tree_id)
        await websocket.send_json({'message': 'Неизвестная ошибка'})
    finally:
        if tree_id:
            manager.disconnect(tree_id, websocket)


@router.websocket("/ws/trees/{tree_id}")
async def websocket_tree_listener(websocket: WebSocket, tree_id: UUID):
    """Подписка на события определенного дерева по id."""
    await websocket.accept()
    await manager.connect(tree_id, websocket)
    logger.info('WebSocket: клиент подписался на обновления дерева %s', tree_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.info('WebSocket: клиент отписался от обновлений дерева %s', tree_id)
        manager.disconnect(tree_id, websocket)