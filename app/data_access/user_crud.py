from datetime import datetime
from typing import Dict

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.schemas import User, UserProfile, UserVerify


async def get_user_by_username(db_session: AsyncSession, username: str):
    """
    Fetches a user row (including password) from priv.chat_history by username.
    Returns a User object or None if no match is found.
    """
    query = select(User).where(User.username == username)
    result = await db_session.execute(query)
    user = result.scalars().first()
    return user


async def save_user(
    db_session: AsyncSession,
    user_id: str,
    username: str,
    password_hash: str,
    role: str,
    tos: bool,
    is_verified: bool,
    meta: Dict[str, str],
    created_date: datetime,
):
    """
    Saves a new user into the priv.users table.
    If the username already exists, raises an IntegrityError.
    """
    try:
        user = User(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            role=role,
            metadata=meta,
            tos=tos,
            is_verified=is_verified,
            created_date=created_date,
        )
        db_session.add(user)
        return user
    except IntegrityError:
        raise ValueError(f"User with username '{username}' already exists.")


async def update_password(
    db_session: AsyncSession,
    username: str,
    password_hash: str,
    updated_date: datetime,
):
    query = (
        update(User)
        .where(User.username == username)
        .values(password_hash=password_hash, updated_date=updated_date)
    )
    await db_session.execute(query)


async def get_user_verify_token(db_session: AsyncSession, username: str):
    query = select(UserVerify.expires_at).where(UserVerify.username == username)
    result = await db_session.execute(query)
    result = result.scalars().first()
    return result


async def save_user_verify_token(
    db_session: AsyncSession, username: str, token: str, expires_at: datetime
):
    uvt = UserVerify(username=username, token=token, expires_at=expires_at)
    db_session.add(UserVerify)


async def save_user_profile(
    db_session: AsyncSession,
    user_id: str,
    persona: str,
    meta: dict,
    created_date: datetime,
):
    user_profile = UserProfile(
        user_id=user_id, persona=persona, meta=meta, created_date=created_date
    )
    db_session.add(user_profile)


async def save_user_verify(
    session: AsyncSession, username: str, is_verified: bool, updated_date: datetime
):
    """
    Updates the user in the database, setting is_verified to 'true'
    and updated_date to the current timestamp.
    """
    query = (
        update(User)
        .where(User.username == username)
        .values(is_verified=is_verified, updated_date=updated_date)
    )
    await session.execute(query)
