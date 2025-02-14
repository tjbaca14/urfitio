from pydantic import BaseModel, EmailStr, field_validator


class UserAuthenticated(BaseModel):
    username: EmailStr
    access_token: str
    refresh_token: str


class RegisterForm(BaseModel):
    username: EmailStr
    password: str
    persona: str
    tos: bool
    meta: dict

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str, info) -> str:
        if isinstance(v, str):
            v = v.lower()
            return v
        return v


class UserRegistered(BaseModel):
    email: str
    token: str


class PasswordResetRequest(BaseModel):
    username: str
    password: str
