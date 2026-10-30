from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/presentation/web/templates")


@router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    """Главная страница с формой создания."""
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.get("/view/{tree_id}", response_class=HTMLResponse)
async def get_tree_page(request: Request, tree_id: str):
    """Страница просмотра и управления конкретным деревом."""
    return templates.TemplateResponse(
        request=request,
        name="tree_view.html",
        context={"tree_id": tree_id}
    )