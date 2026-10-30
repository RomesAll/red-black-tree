from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.application import EventRegistry
from app.application.interfaces import IUnitOfWork
from app.application.use_cases.create_tree_node import CreateNodeUseCase
from app.application.use_cases.delete_tree_node import DeleteTreeNodeUseCase
from app.presentation.api.dependencies import get_uow, get_event_bus
from app.presentation.api.schemas.node import NodeCreateRequest, NodeDeleteRequest
import logging

router = APIRouter(prefix="/trees/{tree_id}/nodes", tags=["Nodes"])
logger = logging.getLogger()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def insert_node(
    tree_id: UUID,
    request: NodeCreateRequest,
    uow: IUnitOfWork = Depends(get_uow),
    event_bus: EventRegistry = Depends(get_event_bus)
):
    """Вставить новый узел в дерево."""
    logger.info('POST запрос на ресурс /trees/{tree_id}/nodes, tree_id=%s, key=%s', tree_id, request.key)
    use_case = CreateNodeUseCase(uow=uow, event_registry=event_bus)
    await use_case.execute(
        tree_id=tree_id,
        key=request.key,
        value=request.value
    )
    logger.info('Узел key=%s успешно добавлен в дерево %s', request.key, tree_id)
    return {"status": "ok", "message": "Node inserted"}


@router.delete("/")
async def delete_node(
    tree_id: UUID,
    request: NodeDeleteRequest,
    uow: IUnitOfWork = Depends(get_uow),
    event_bus: EventRegistry = Depends(get_event_bus)
):
    """Удалить узел из дерева по ключу."""
    logger.info('DELETE запрос на ресурс /trees/{tree_id}/nodes, tree_id=%s, key=%s', tree_id, request.key)
    use_case = DeleteTreeNodeUseCase(uow=uow, event_register=event_bus)
    await use_case.execute(tree_id=tree_id, key=request.key)
    logger.info('Узел key=%s успешно удален из дерева %s', request.key, tree_id)
    return {"status": "ok", "message": "Node deleted"}