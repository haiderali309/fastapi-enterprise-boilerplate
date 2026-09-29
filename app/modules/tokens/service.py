from datetime import datetime, timedelta , timezone
import secrets
from .repository import create_token ,revoke_token
from .enums import TokenType
from app.shared.security.hashing import hash_token
from .schemas import TokenCreate
from app.core.config import settings
from .repository import get_token
from app.core.logging import logger
from .exception import TokenExpired, TokenNotExists
from app.core.exception_handlers import AppExceptionHandler


def generate_token():
    return secrets.token_urlsafe(32)


async def create_refresh_token( db, user_id:int ):

    raw_token = generate_token()

    await create_token( db, 
                       TokenCreate(
                           user_id=user_id,
                           token_hash=hash_token(raw_token),
                           token_type=TokenType.REFRESH,
                           expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRY_DAYS)
                        )
    )

    return raw_token



async def create_email_verify_token( db, user_id:int ):

    raw_token = generate_token()

    await create_token( db,
                       TokenCreate(
                           user_id=user_id,
                           token_hash=hash_token(raw_token),
                           token_type=TokenType.EMAIL_VERIFY,
                           expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.EMAIL_VERIFY_TOKEN_EXPIRY_MINUTE)
                        )
    )

    return raw_token



async def create_password_reset_token( db, user_id:int ):

    raw_token = generate_token()

    await create_token( db,
                       TokenCreate(
                           user_id=user_id,
                           token_hash=hash_token(raw_token),
                           token_type=TokenType.PASSWORD_RESET,
                           expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.PASSWORD_RESET_EXPIRY_MINUTE)
                       )
    )

    return raw_token


async def get_token_service(db, token_hash: str, token_type: TokenType ):

    try:

        token_record = await get_token(db, token_hash, token_type)

        if not token_record:
            raise TokenNotExists()

        expires_at = token_record.expires_at
        if expires_at.tzinfo is None:
            now = datetime.utcnow()
        else:
            now = datetime.now(timezone.utc)

        if now >= expires_at:
            raise TokenExpired()

        return token_record
    
    except AppExceptionHandler:
        # Re-raise custom app exceptions directly
        raise
    except Exception:
        logger.error("Failed while checking token")
        raise
    



async def revoke_token_service( db, token_id:int ):

    try:

        record = await revoke_token(db, token_id)

        if record:
            return record
        
    except Exception:
            logger.error("Failed while revoking token")
            raise