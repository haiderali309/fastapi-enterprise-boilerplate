from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)
from app.core.config import settings

engine=create_async_engine(settings.DATABASE_URL , echo=True)

Local_Session=async_sessionmaker(expire_on_commit=False , bind=engine)

async def get_db():
    async with Local_Session() as db:
        yield db
