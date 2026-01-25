from typing import AsyncGenerator

from app.common.clients.http_client import HTTPClient
from fastapi import Request


async def get_http_client(request: Request) -> HTTPClient:
    return request.app.state.http_client


async def get_db_session(request: Request) -> AsyncGenerator[AsyncGenerator, None]:
    async with request.app.state.db.session() as session:
        yield session
