from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import settings

# -----------------------------------------------------------------------------
# Database Engine & Session Factory
# -----------------------------------------------------------------------------
# Create asynchronous engine connected to database defined in settings.DATABASE_URL
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Async session maker factory used for generating database sessions
Local_Session = async_sessionmaker(expire_on_commit=False, bind=engine)


async def get_db():
    """
    FastAPI dependency yielding an async database session per request.
    Automatically closes the session when the request context finishes.
    """
    async with Local_Session() as db:
        yield db
