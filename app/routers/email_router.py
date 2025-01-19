from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Response, Query, Body
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authentication import verify_access_token, verify_or_refresh_factory
from app.dependencies import get_auth_service, get_db_session, get_email_service
from app.services.auth_service import AuthenticationService
from app.services.email_service import EmailService
from app.models.email_verification import EmailVerificationRequest
from app.utils import AuthenticationError, get_logger

templates = Jinja2Templates(directory="app/templates")

email_router = APIRouter(tags=["Email Verification"])

logger = get_logger(__name__)

@email_router.get(
    "/email-verification/verify",
)
async def verify_email(
    email: str = Query(...),
    token: str = Query(...),
    email_service: EmailService = Depends(get_email_service),
    db_session: AsyncSession = Depends(get_db_session),
):
    try:
        # TODO: Make this a background task and response 200 on success
        await email_service.verify_email(db_session, email, token)
        return RedirectResponse("/email-verification/success")
    except Exception as e:
        return RedirectResponse("/email-verification/error")


@email_router.post(
    "/email-verification/send", 
    # dependencies=[Depends(verify_access_token)
                #   ]
)
async def send_verification_email(
    ev_request: EmailVerificationRequest,
    email_service: EmailService = Depends(get_email_service),
    db_session: AsyncSession = Depends(get_db_session),
):
    template = templates.get_template("/email/email_template.html")
    # try:
    await email_service.send_email(
        db_session, html_template=template, email_verification_request=ev_request
    )
    # except AuthenticationError:
    #     logger.inf
    #     return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request ")


@email_router.post(
    "/email-verification/resend", dependencies=[Depends(verify_access_token)]
)
async def send_verification_email(
    ev_request: EmailVerificationRequest = Body(...),
    email_service: EmailService = Depends(get_email_service),
    db_session: AsyncSession = Depends(get_db_session),
):
    template = templates.get_template("/email/email_template.html")
    try:
        await email_service.send_email(
            db_session, html_template=template, email_verification_request=ev_request
        )
    except Exception as e:
        logger.exception(f"Email failed: {str(e)}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Request failed with {str(e)}")
    
@email_router.post(
    "/password-reset-email"
)
async def send_password_reset_email(
    email: dict = Body(...),
    email_service: EmailService = Depends(get_email_service),
    db_session: AsyncSession = Depends(get_db_session),
):
    template = templates.get_template("/email/email_password_reset.html")
    await email_service.send_password_reset_email(
        db_session, template=template, email=email
    )
        
