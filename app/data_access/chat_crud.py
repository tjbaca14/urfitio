from datetime import datetime
from typing import Dict, List

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_access.schemas import ChatHistory


async def save_chat(db_session: AsyncSession, id: str, user_id: str, messages: List[dict], created_date: datetime):
    chat_history = ChatHistory(
        id=id, user_id=user_id, messages=messages, created_date=created_date
    )
    await db_session.merge(chat_history)