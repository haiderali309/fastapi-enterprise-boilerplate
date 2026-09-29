from datetime import datetime , timezone
from sqlalchemy import select, update
from .models import Token
from .enums import TokenType
from .schemas import TokenCreate
from app.core.logging import logger



async def create_token(db,data: TokenCreate):

    try:
        token = Token(**data.model_dump())
        db.add(token)
        await db.commit()
        await db.refresh(token)
        return token

    except Exception :
        await db.rollback()
        logger.error("Error to create token")
        raise


async def get_token(db, token_hash: str, token_type: TokenType ):

    try:
        query = select(Token).where( Token.token_hash == token_hash, Token.token_type == token_type, Token.revoked == False )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    except Exception:
        logger.error("Error while searching Token")
        raise


async def revoke_token( db, token_id:int ):

    try:
        query = (update(Token).where(Token.id == token_id).values(revoked=True,used_at=datetime.now(timezone.utc)))
        result = await db.execute(query)
        await db.commit()
        return result.rowcount > 0
    except Exception:
        logger.error("Error while updating Token")
        raise