from datetime import datetime
from typing import Dict

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.schemas import ChatHistory, User


async def save_chat_history(
    db_session: AsyncSession,
    id: str,
    user_id: str,
    messages: list[dict],
    created_date: datetime,
    updated_date: str,
):
    chat_history = ChatHistory(
        id=id,
        user_id=user_id,
        messages=messages,
        created_date=created_date,
        updated_date=updated_date,
    )
    db_session.merge(chat_history)
    return chat_history
