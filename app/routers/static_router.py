from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.util import get_logger

logger = get_logger(__name__)

static_router = APIRouter(tags=["Static"])

templates = Jinja2Templates(directory="app/templates")

static_router.mount("/static", StaticFiles(directory="app/static"), name="static")


@static_router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})