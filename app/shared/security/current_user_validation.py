from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .jwt import decode_access_token
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.models import Users
from sqlalchemy import select
from .exception import UserNotActive , UserNotFound

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
TOKEN = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(token: TOKEN, db: AsyncSession = Depends(get_db)):

    payload = decode_access_token(token)

    if not payload:
        raise UserNotFound()

    user_id = int(payload["sub"])
    
    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
        
    if not user.is_active:
        raise UserNotActive
    return user