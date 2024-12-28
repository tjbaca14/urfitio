import httpx
from fastapi import Depends, Request

from app.config import ClaudeConfig, claude_config
from app.services.claude_service import ClaudeAPI


async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

async def get_claude_config() -> ClaudeConfig:
    return claude_config

async def get_cache(request: Request) -> dict:
    return request.app.state.cache

async def get_claude_api(
    http_client: httpx.AsyncClient = Depends(get_http_client),
    claude_config: ClaudeConfig = Depends(get_claude_config),
) -> ClaudeAPI:
    return ClaudeAPI(config=claude_config, http_client=http_client)
