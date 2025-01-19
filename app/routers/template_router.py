from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.authentication import verify_or_refresh_factory, verify_access_token
from app.utils import get_logger

logger = get_logger(__name__)

template_router = APIRouter(tags=["Templates"])

templates = Jinja2Templates(directory="app/templates")

scopes = ["user"]

verify_or_refresh_dep = Depends(verify_or_refresh_factory(required_scopes=scopes))

async def validate_user_access_token(email: str = Query(...), token:str = Query(...)) -> str:
    try:
        token = verify_access_token(token)
        if token.get("sub") == email:
            return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/password-reset-request"},
        )

@template_router.get("/", dependencies=[verify_or_refresh_dep])
async def redirect_user(request: Request):
    """
    If authenticated -> /login
    else -> /chat
    """
    return RedirectResponse(url="/chat")


@template_router.get(
    "/chat",
    response_class=HTMLResponse,
)
async def get_main_page(
    request: Request,
    username: str = verify_or_refresh_dep,
):
    # need to extract username from cookie or request objecet depending on where we store it
    # use token extraction?
    return templates.TemplateResponse(
        "chat.html", {"request": request, "username": username}
    )


@template_router.get(
    "/about", response_class=HTMLResponse, 
    # dependencies=[verify_or_refresh_dep]
)
async def get_about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@template_router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("/authenticate/login.html", {"request": request})


@template_router.get("/email-verification/pending", response_class=HTMLResponse)
async def get_verify_page(request: Request, email: str = Query(...)):
    return templates.TemplateResponse("/email/email_pending.html", {"request": request, "email": email})


@template_router.get("/email-verification/success", response_class=HTMLResponse)
async def get_verified_page(request: Request):
    return templates.TemplateResponse(
        "/email/email_verified.html", {"request": request}
    )


@template_router.get("/email-verification/unverified", response_class=HTMLResponse)
async def get_unverified_page(request: Request):
    return templates.TemplateResponse(
        "/emaile/email_unverified.html", {"request": request}
    )


@template_router.get("/email-verification/error", response_class=HTMLResponse)
async def get_error_page(request: Request):
    return templates.TemplateResponse("/email/email_error.html", {"request": request})


@template_router.get("/register", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse(
        "/authenticate/register.html", {"request": request}
    )


@template_router.get("/password-reset-request", response_class=HTMLResponse)
async def get_password_reset_request_page(request: Request,
                          ):
    return templates.TemplateResponse(
        "/authenticate/password_reset_request.html", {"request": request}
    )

@template_router.get("/password-reset", response_class=HTMLResponse)
async def get_password_reset(request: Request,
                             token: dict = Depends(validate_user_access_token)
                          ):
        return templates.TemplateResponse(
            "/authenticate/password_reset.html", {"request": request}
        )


@template_router.get("/verify-email", response_class=HTMLResponse)
async def get_verify_email_page(request: Request):
    return templates.TemplateResponse(
        "/email/email_template.html",
        {"request": request, "verification_link": "something", "email": "abcde"},
    )

@template_router.get("/terms-of-service", response_class=HTMLResponse)
async def get_password_reset(request: Request,
                          ):
        return templates.TemplateResponse(
            "/tos.html", {"request": request}
        )

@template_router.get("/privacy-policy", response_class=HTMLResponse)
async def get_password_reset(request: Request,
                          ):
        return templates.TemplateResponse(
            "/pp.html", {"request": request}
        )