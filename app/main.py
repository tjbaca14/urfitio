from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Response

from app.chat import chat_router
from app.coaches import coach_router
from app.startup import ApplicationContainer
from app.utils import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize application container
    container = ApplicationContainer()
    await container.initialize()
    app.state.db = container.db
    app.state.http_client = container.http_client
    app.state.llm_provider = container.llm_provider
    app.state.cache = container.cache

    yield

    # Clean up resources
    await container.close()


app = FastAPI(tags=["UrFitIO"], lifespan=lifespan)


@app.get("/health")
async def health_check():
    return Response(content="ok", status_code=200)


app.include_router(chat_router)
app.include_router(coach_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
