from typing import Annotated
from fastapi import Depends
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.security.current_user_validation import get_current_user
from app.modules.users.models import Users

DB_SESSION=Annotated[AsyncSession,Depends(get_db)]

user_dependency=Annotated[Users,Depends(get_current_user)]