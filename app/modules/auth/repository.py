from sqlalchemy import select , update
from app.modules.users.models import Users
from app.core.logging import logger

async def check_user_email(db,email):
    try:
        result= await db.execute(select(Users).where(Users.email==email))
        return result.scalar_one_or_none()

    except Exception:
        logger.error("Error checking user email")
        raise

async def check_user_username(db,username):
    try:
        result = await db.execute(select(Users).where(Users.username == username))
        return result.scalar_one_or_none()
    
    except Exception :
        logger.error("Error checking user username")
        raise


async def save_user(db,data):
    try:
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return data

    except Exception :
        await db.rollback()
        logger.error("Error saving user")
        raise

async def verify_user_email(db,user_id):
    try:
        query=(update(Users).where(Users.id==user_id).values(is_verified=True))
        result = await db.execute(query)
        await db.commit()
        return result.rowcount > 0
    except Exception:
        logger.error("Error while verify user status")
        raise

async def get_user_by_id(db, user_id: int):
    try:
        query = select(Users).where(Users.id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except Exception:
        logger.error("Error getting user by ID")
        raise

async def update_user_password(db, user_id: int, hashed_password: str):
    try:
        query = update(Users).where(Users.id == user_id).values(hash_password=hashed_password)
        result = await db.execute(query)
        await db.commit()
        return result.rowcount > 0
    except Exception:
        await db.rollback()
        logger.error("Error updating user password")
        raise

