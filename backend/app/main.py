from contextlib import asynccontextmanager

import uvicorn
from app.chat.routes import chat_router
from app.common.exception_handlers import register_exception_handlers
from app.ncaa import divisions_router, schools_router
from app.startup import ApplicationContainer
from app.utils import get_logger
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = ApplicationContainer()
    await container.initialize()
    app.state.db = container.db
    app.state.http_client = container.http_client
    app.state.llm_provider = container.llm_provider
    app.state.cache_client = container.cache_client
    app.state.school_cache_service = container.school_cache_service

    yield

    await container.close()


app = FastAPI(tags=["UrFitIO"], lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)


@app.get("/health")
async def health_check():
    return Response(content="ok", status_code=200)


app.include_router(chat_router)
app.include_router(divisions_router)
app.include_router(schools_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
