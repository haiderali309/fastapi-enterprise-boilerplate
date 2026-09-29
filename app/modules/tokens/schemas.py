from datetime import datetime
from pydantic import BaseModel
from .enums import TokenType


class TokenCreate(BaseModel):

    user_id: int
    token_hash: str
    token_type: TokenType
    expires_at: datetime


class LoginTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str
