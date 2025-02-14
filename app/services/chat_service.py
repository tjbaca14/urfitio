from datetime import datetime
from typing import Dict

import pytz
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.chat_crud import save_chat
from app.models.chat import ChatRequest, Message
from app.services.llm_service import LLMApi
from app.utils import get_logger

logger = get_logger(__name__)


async def rag_service(
    cache: Dict[str, str], chat_request: ChatRequest, llm_api: LLMApi
) -> Message:
    # retrieve context
    messages = chat_request.messages

    context = _retrieve_context(cache, chat_request.contextQuery)

    logger.info(f"context: {context}")
    # pass context into school name
    user_query = f"User query: {chat_request.messages[-1]}"
    message_context = f"Context: <data>{context}<data>\n\n"

    messages[-1].content = message_context + user_query
    resp = await llm_api.generate(messages)
    return resp


def _retrieve_context(data: dict, context_query: dict) -> str:
    # this is brutal but oh well for now
    # wont be querying dictionaries for long so we'll live with it
    # .... famous last words
    data = data.get(context_query.get("division")).get(context_query.get("school"))
    return data


async def save_chat_service(
    db_session: AsyncSession,
    chat_request: ChatRequest,
) -> Message:
    messages = [message.model_dump() for message in chat_request.messages]
    await save_chat(
        db_session,
        chat_request.id,
        chat_request.userId,
        messages,
        created_date=datetime.now(pytz.timezone("America/Los_Angeles")),
    )
    return chat_request
