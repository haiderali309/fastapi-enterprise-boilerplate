from typing import Annotated
from fastapi import Depends
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

DB_SESSION=Annotated[AsyncSession,Depends(get_db)]