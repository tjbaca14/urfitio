from typing import AsyncGenerator

import boto3
import httpx
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import (EmailSettings, LLMConfig, email_settings,
                             llm_config)
from app.services.auth_service import AuthenticationService
from app.services.email_service import EmailService
from app.services.llm_service import LLMApi


async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


async def get_llm_config() -> LLMConfig:
    return llm_config


async def get_cache(request: Request) -> dict:
    return request.app.state.cache


async def get_llm_api(
    http_client: httpx.AsyncClient = Depends(get_http_client),
    llm_config: LLMConfig = Depends(get_llm_config),
) -> LLMApi:
    return LLMApi(config=llm_config, http_client=http_client)


async def get_db_session(request: Request) -> AsyncGenerator[AsyncGenerator, None]:
    async with request.app.state.db.session() as session:
        yield session


async def get_db_no_commit_session(
    request: Request,
) -> AsyncGenerator[AsyncGenerator, None]:
    async with request.app.state.db.session(autocommit=False) as session:
        yield session


async def get_auth_service() -> AuthenticationService:
    return AuthenticationService()


async def get_email_client() -> boto3.client:
    # coupled to ses but oh well
    return boto3.client("ses", region_name="us-west-2")


async def get_email_settings() -> EmailSettings:
    return email_settings


async def get_email_service(
    email_client: boto3.client = Depends(get_email_client),
    email_settings: EmailSettings = Depends(get_email_settings),
) -> EmailService:
    return EmailService(
        email_client, email_settings.source_email, email_settings.source_domain
    )
