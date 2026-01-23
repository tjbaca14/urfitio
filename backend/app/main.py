from contextlib import asynccontextmanager

import uvicorn
from app.chat.routes import chat_router
from app.ncaa import divisions_router, schools_router
from app.startup import ApplicationContainer
from app.utils import get_logger
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize application container
    container = ApplicationContainer()
    await container.initialize()
    app.state.db = container.db
    app.state.http_client = container.http_client
    app.state.llm_provider = container.llm_provider
    app.state.cache_client = container.cache_client
    app.state.school_cache_service = container.school_cache_service

    yield

    # Clean up resources
    await container.close()


app = FastAPI(tags=["UrFitIO"], lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://0.0.0.0:3000",  # 0.0.0.0 binding
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/health")
async def health_check():
    return Response(content="ok", status_code=200)


app.include_router(chat_router)
app.include_router(divisions_router)
app.include_router(schools_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
