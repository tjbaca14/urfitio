from typing import Dict

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authentication import verify_or_refresh_factory
from app.dependencies import get_cache, get_db_session, get_llm_api
from app.models.chat import ChatRequest, Message
from app.services.chat_service import rag_service, save_chat_service
from app.services.llm_service import LLMApi
from app.utils import get_logger

logger = get_logger(__name__)

chat_router = APIRouter(
    prefix="/api/v1",
    tags=["Chat"],
)


@chat_router.post("/chat", response_model=Message)
async def chat_endpoint(
    chat_request: ChatRequest,
    response: Response,
    cache: Dict[str, str] = Depends(get_cache),
    llm_api: LLMApi = Depends(get_llm_api),
    user: str = Depends(verify_or_refresh_factory(required_scopes=["user"])),
) -> Message:
    # logger.info(f"Input messages: {chat_request}")
    resp = await rag_service(cache=cache, chat_request=chat_request, llm_api=llm_api)
    return resp


@chat_router.post("/save/chat", response_model=ChatRequest)
async def chat_endpoint(
    chat_request: ChatRequest,
    response: Response,
    db_session: AsyncSession = Depends(get_db_session),
    user: str = Depends(verify_or_refresh_factory(required_scopes=["user"])),
) -> ChatRequest:
    # logger.info(f"Input messages: {chat_request}")
    await save_chat_service(db_session, chat_request=chat_request)
    return chat_request
