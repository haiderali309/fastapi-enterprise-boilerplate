from datetime import datetime, timedelta , timezone
from jose import jwt, JWTError
from app.core.config import settings
from app.core.logging import logger


SECRET_KEY = settings.JWT_SECRET

ALGORITHM = settings.JWT_ALGO

EXPIRE_TIME_MINUTES=settings.ACCESS_TOKEN_EXPIRY_MINUTE



def create_access_token( user_id: int, user_role : str ):

    payload = {
        "sub": str(user_id),
        "type": "access",
        "role": user_role,
        "exp": datetime.now(timezone.utc) + timedelta(EXPIRE_TIME_MINUTES)
        }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def decode_access_token( token: str ):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "access":
            return None

        return payload

    except JWTError as e:
        logger.error(f"The token decode Failed:{e}")
        return None