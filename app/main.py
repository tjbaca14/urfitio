from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers.chat_router import chat_router
from app.routers.crud_router import crud_router
from app.services.cache_service import create_cache
from app.util import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: modularize
    app.state.cache = await create_cache()
    async with httpx.AsyncClient() as client:
        logger.info("Setting up HTTP client...")
        app.state.http_client = client  # singleton
        logger.info("HTTP client setup complete")
        yield
        logger.info("Closing HTTP client...")
        await app.state.http_client.aclose()
        logger.info("HTTP client closed")


app = FastAPI(tags=["RecruitIO"], lifespan=lifespan)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    return Response(content="ok", status_code=200)


app.include_router(crud_router)
app.include_router(chat_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
