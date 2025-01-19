from datetime import datetime
import uuid
from typing import Union

import pytz
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authentication import create_access_token
from app.core.config import auth_settings
from app.data_access.user_crud import (
    get_user_by_username,
    save_user,
    save_user_profile,
    update_password,
)
from app.models.auth_models import (
    RegisterForm,
    UserAuthenticated,
    UserRegistered,
    PasswordResetRequest,
)
from app.utils import AuthenticationError, RegistrationError, EntityNotFoundError
from sqlalchemy.exc import IntegrityError
from app.utils import get_logger
logger = get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:
    """
    Used to register and authenticate users
    """

    async def authenticate_user(
        self,
        db_session: AsyncSession,
        username: str,
        password: str,
        scope: str = "user",
    ) -> UserAuthenticated:
        user = await get_user_by_username(db_session=db_session, username=username)
        logger.info(f"USER {user}")
        if user:
            password_verified = self._verify_password(password, user.password_hash)
            logger.info(f"password verified {password_verified}")
        if not user or not password_verified or not user.is_verified:
            logger.info("Bad creds")
            raise AuthenticationError

        return UserAuthenticated(
            username=username,
            access_token=create_access_token(
                data={"sub": user.username, "scope": scope},
                expires_delta=auth_settings.access_token_expire_minutes,
            ),
            refresh_token=create_access_token(
                data={"sub": user.username, "scope": scope},
                expires_delta=auth_settings.refresh_token_expire_days,
            ),
        )

    async def register_user(
        self, db_session: AsyncSession, register_form: RegisterForm, role: str
    ) -> UserRegistered:
        try:
            user_id = str(uuid.uuid4())
            password_hash = self._get_password_hash(register_form.password)
            created_date = datetime.now(pytz.timezone("America/Los_Angeles"))

            await save_user(
                db_session=db_session,
                user_id=user_id,
                username=register_form.username,
                role=role,
                tos=register_form.tos,
                meta=register_form.meta,
                password_hash=password_hash,
                is_verified=False,
                created_date=created_date,
            )
            await save_user_profile(
                db_session=db_session,
                user_id=user_id,
                persona=register_form.persona,
                meta=register_form.meta,
                created_date=created_date,
            )
            await db_session.commit()

            token = create_access_token(
                data={"sub": register_form.username, "scope": "email"},
                expires_delta=auth_settings.signup_token_expire_minutes,
            )  # issue shortlived email token
            user_registed = UserRegistered(email=register_form.username, token=token)

            return user_registed
        except IntegrityError:
            raise RegistrationError

    async def password_reset(
        self, db_session: AsyncSession, pw_reset_request: PasswordResetRequest
    ) -> bool:
        user = await get_user_by_username(
            db_session, username=pw_reset_request.password
        )
        if user:
            password_hash = self._get_password_hash(pw_reset_request.password)
            await update_password(db_session, user.username, password_hash)
            return True
        raise EntityNotFoundError

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
