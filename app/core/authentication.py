from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import Depends, HTTPException, Request, Response, status
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import auth_settings
from app.utils import get_logger

logger = get_logger(__name__)

'''
Theres some wonkinees due to SSR and browser interaction.
The core to do Ouath2 is here. 
Will refactor when we move to proper UI framework
'''

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=5))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM
    )
    return encoded_jwt


def get_token_from_cookies(request: Request, token_name: str) -> str:
    """
    Retrieves a token from cookies by name.
    Raises 401 if missing.
    """
    token = request.cookies.get(token_name)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{token_name} missing"
        )
    return token

def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        return decoded
    except ExpiredSignatureError:
        raise ValueError("Invalid token")
    except JWTError:
        raise ValueError("Invalid token")
    except Exception:
        raise ValueError("Invalid token")

def decode_and_validate_token(
    token: str,
    token_type: str,
    secret_key: str,
    algorithms: list[str],
    required_scopes: list = [],
) -> dict:
    """
    Decodes and validates a JWT.
    Raises 401 if invalid or expired.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        username = payload.get("sub")
        scope = payload.get("scope")
        allowed = scope in required_scopes
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid {token_type}",
            )
        if required_scopes and not allowed:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unauthorized scope.",
            )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{token_type} expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid {token_type}"
        )


def get_refresh_token(request: Request) -> str:
    """
    Retrieves refresh_token from cookies.
    """
    return get_token_from_cookies(request, "refresh_token")


def get_access_token(request: Request) -> str:
    return get_token_from_cookies(request, "access_token")

def verify_refresh_token(
    refresh_token: str = Depends(get_refresh_token),
) -> str:
    """
    Decodes and validates the refresh token.
    Returns the username (sub) if valid.
    """
    payload = decode_and_validate_token(
        refresh_token,
        "refresh_token",
        auth_settings.SECRET_KEY,
        [auth_settings.ALGORITHM],
    )
    return payload["sub"]


def verify_access_token(access_token: str = Depends(get_access_token)) -> str:
    payload = decode_and_validate_token(
        access_token,
        "access_token",
        auth_settings.SECRET_KEY,
        [auth_settings.ALGORITHM],
    )
    return payload


async def verify_or_refresh(
    request: Request,
    response: Response,
    required_scopes: List[str],
    redirect: str = None,
) -> str:
    """
    Checks if the access token is valid.
    If not, tries the refresh token to generate a new access token.
    """
    try:
        # Attempt to verify the access token
        access_token = get_token_from_cookies(request, "access_token")
        payload = decode_and_validate_token(
            access_token,
            "access token",
            auth_settings.SECRET_KEY,
            [auth_settings.ALGORITHM],
            required_scopes=required_scopes,
        )
        return payload["sub"]
    except ExpiredSignatureError:
        pass
    except JWTError:
        pass
    except HTTPException as e:
        pass
    try:
        logger.debug("Access token expired attempting refresh")
        # Attempt to verify the refresh token and generate a new access token
        refresh_token = get_token_from_cookies(request, "refresh_token")
        payload = decode_and_validate_token(
            refresh_token,
            "refresh token",
            auth_settings.SECRET_KEY,
            [auth_settings.ALGORITHM],
            required_scopes=required_scopes,
        )
        username = payload["sub"]
        new_access = create_access_token(
            data={"sub": username},
            expires_delta=auth_settings.access_token_expire_minutes,
        )
        response.set_cookie(
            key="access_token",
            value=new_access,
            httponly=True,
            # secure=True, samesite="strict", etc. in production #TODO: FIX BEFORE PROD
        )
        return username
    except HTTPException:
        return _redirect_handler(request, redirect)
    except ExpiredSignatureError:
        return _redirect_handler(request, redirect)
    except JWTError:
        return _redirect_handler(request, redirect)
    except Exception:
        return _redirect_handler(request, redirect)


def _redirect_handler(request: Request, redirect: str = None):
    """
    Helper function to either raise 401 or
    return a RedirectResponse to the login page.
    """
    if request.headers.get("accept") == "application/json":
        # Return JSON response for API requests
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please log in again.",
        )
    else:
        # Redirect for SSR requests
        if not redirect:
            redirect = "/login"
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/login"},
        )


def verify_or_refresh_factory(required_scopes: List[str], redirect: str = None):
    """
    Returns a dependency that calls verify_or_refresh with a specific scope.
    """

    async def dependency(request: Request, response: Response) -> str:
        return await verify_or_refresh(
            request, response, required_scopes=required_scopes, redirect=redirect
        )

    return dependency
