
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database.base import Base


class Token(Base):

    __tablename__ = "user_tokens"

    id = Column( Integer, primary_key=True )

    user_id = Column( Integer, ForeignKey( "users.id", ondelete="CASCADE" ), nullable=False )

    token_hash = Column( String(255), nullable=False, unique=True)

    token_type = Column( String(100), nullable=False )

    expires_at = Column( DateTime(timezone=True), nullable=False )

    revoked = Column( Boolean, default=False )

    used_at = Column( DateTime(timezone=True), nullable=True )


    created_at = Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )

    updated_at = Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )