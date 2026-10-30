import logging
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.application.interfaces import IUnitOfWork
from app.application.use_cases.create_tree import CreateTreeUseCase
from app.application.use_cases.get_tree import GetTreeUseCase
from app.application.use_cases.delete_tree import DeleteTreeUseCase
from app.domain.exceptions import TreeNotFoundError
from app.presentation.api.dependencies import get_uow
from app.presentation.api.schemas.tree import TreeCreateRequest, TreeResponse

router = APIRouter(prefix="/trees", tags=["Trees"])
logger = logging.getLogger()


@router.post("/", response_model=TreeResponse, status_code=status.HTTP_201_CREATED)
async def create_tree(
        request: TreeCreateRequest,
        uow: IUnitOfWork = Depends(get_uow)
):
    """Создать новое дерево (опционально с начальными данными)."""
    logger.info('POST запрос на ресурс /trees')
    use_case = CreateTreeUseCase(uow=uow)
    tree_id = await use_case.execute(raw_data=request.initial_data)

    # Получить созданное дерево
    get_use_case = GetTreeUseCase(uow=uow)
    tree = await get_use_case.execute(tree_id)
    logger.info('Дерево %s успешно создано, корень %s', tree['tree_id'], tree['root'])
    return TreeResponse(
        tree_id=tree['tree_id'],
        size=tree['size'],
        root=tree['root']
    )


@router.get("/{tree_id}", response_model=TreeResponse)
async def get_tree(
        tree_id: UUID,
        uow: IUnitOfWork = Depends(get_uow)
):
    """Получить информацию о дереве."""
    logger.info('GET запрос на ресурс /trees/%s', tree_id)
    use_case = GetTreeUseCase(uow=uow)
    tree = await use_case.execute(tree_id)

    return TreeResponse(
        tree_id=tree['tree_id'],
        size=tree['size'],
        root=tree['root']
    )


@router.delete("/{tree_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tree(
        tree_id: UUID,
        uow: IUnitOfWork = Depends(get_uow)
):
    """Удалить дерево целиком."""
    logger.info('DELETE запрос на ресурс /trees/{tree_id}, tree_id=%s', tree_id,)
    use_case = DeleteTreeUseCase(uow=uow)
    await use_case.execute(tree_id)
    logger.info('Дерево %s успешно удалено', tree_id)
    return {'message': 'ok'}