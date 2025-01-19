from pydantic import BaseModel, EmailStr


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


class UserRegistered(BaseModel):
    email: str
    token: str


class PasswordResetRequest(BaseModel):
    username: str
    password: str
