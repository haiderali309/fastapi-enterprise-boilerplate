from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.users.models import Users
from typing import List, Optional
from app.core.logging import logger


async def get_all_users_repo(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Users]:
    try:
        result = await db.execute(select(Users).offset(skip).limit(limit))
        return result.scalars().all()
    except Exception:
        logger.error("Error fetching all users")
        raise


async def get_user_by_id_repo(db: AsyncSession, user_id: int) -> Optional[Users]:
    try:
        result = await db.execute(select(Users).where(Users.id == user_id))
        return result.scalar_one_or_none()
    except Exception:
        logger.error(f"Error fetching user by ID {user_id}")
        raise


async def update_user_repo(db: AsyncSession, user: Users, data: dict) -> Users:
    try:
        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception:
        await db.rollback()
        logger.error("Error updating user")
        raise


async def delete_user_repo(db: AsyncSession, user: Users) -> None:
    try:
        await db.delete(user)
        await db.commit()
    except Exception:
        await db.rollback()
        logger.error("Error deleting user")
        raise
