from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

from app.routers.auth_router import auth_router
from app.routers.chat_router import chat_router
from app.routers.crud_router import crud_router
from app.routers.email_router import email_router
from app.routers.template_router import template_router
from app.services.cache_service import create_cache
from app.startup import init_db
from app.utils import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: modularize
    app.state.cache = await create_cache()
    app.state.db = init_db()
    async with httpx.AsyncClient() as client:
        logger.info("Setting up HTTP client...")
        app.state.http_client = client  # singleton
        logger.info("HTTP client setup complete")
        yield
        logger.info("Closing HTTP client...")
        await app.state.http_client.aclose()
        logger.info("HTTP client closed")


app = FastAPI(tags=["RecruitIO"], lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/health")
async def health_check():
    return Response(content="ok", status_code=200)


app.include_router(crud_router)
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(template_router)
app.include_router(email_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
