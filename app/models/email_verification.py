from pydantic import BaseModel


class EmailVerificationRequest(BaseModel):
    email: str
    token: str | None = None
