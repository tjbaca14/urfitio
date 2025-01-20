import json

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import auth_settings
from app.dependencies import get_auth_service, get_db_no_commit_session, get_db_session
from app.models.auth_models import RegisterForm, PasswordResetRequest
from app.services.auth_service import AuthenticationService
from app.utils import (
    AuthenticationError,
    RegistrationError,
    EntityNotFoundError,
    get_logger,
)

logger = get_logger(__name__)
auth_router = APIRouter(tags=["Authenticate"], prefix="/api/v1")


async def parse_register_form(
    username: str = Form(...),
    password: str = Form(...),
    persona: str = Form(...),
    meta: str = Form(...),
    tos: bool = Form(...),
) -> RegisterForm:
    try:
        return RegisterForm(
            username=username, password=password, persona=persona, meta=json.loads(meta), tos=tos
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid form data: {str(e)}")


async def parse_password_reset_form(
    username: str = Form(...), password: str = Form(...)
) -> PasswordResetRequest:
    try:
        return PasswordResetRequest(username=username, password=password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid form data: {str(e)}")


@auth_router.post("/token")
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends(get_auth_service),
    db_session: AsyncSession = Depends(get_db_session),
):
    try:
        user = await auth_service.authenticate_user(
            db_session, request.username, request.password
        )
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    response = JSONResponse(
        content={"username": user.username}, status_code=status.HTTP_200_OK
    )
    response.set_cookie(
        "access_token",
        user.access_token,
        httponly=True,
        secure=True,
        max_age=auth_settings.access_token_expire_minutes * 60,
        samesite="Strict",
    )
    response.set_cookie(
        "refresh_token",
        user.refresh_token,
        httponly=True,
        secure=True,
        max_age=auth_settings.refresh_token_expire_days * 86400,
        samesite="Strict",
    )
    return response


@auth_router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.status_code = 200
    response.headers["Location"] = "/login"
    return response


@auth_router.post("/register")
async def register_user(
    register_form: RegisterForm = Depends(parse_register_form),
    auth_service: AuthenticationService = Depends(get_auth_service),
    db_session: AsyncSession = Depends(get_db_no_commit_session),
):
    logger.info(f"Recieved signup request for {register_form}")
    try:
        user = await auth_service.register_user(
            db_session=db_session, register_form=register_form, role="user"
        )
        response = JSONResponse(
            content=user.model_dump(), status_code=status.HTTP_200_OK
        )
        return response
    except RegistrationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The username is already taken. Please choose a different one.",
        )


@auth_router.post("/password-reset")
async def reset_password(
    password_reset_request: PasswordResetRequest,
    db_session: AsyncSession = Depends(get_db_session),
    
    auth_service: AuthenticationService = Depends(get_auth_service),
):
    try:
        auth_service.password_reset(db_session, password_reset_request)
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found with the provided username",
        )
