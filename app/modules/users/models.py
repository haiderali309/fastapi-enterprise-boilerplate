from app.database.base import Base
from sqlalchemy import Column, INTEGER, String, BOOLEAN, func, DateTime
from app.authorization.roles import Role


class Users(Base):
    """
    Core User entity model representing system users.
    """
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)

    role = Column(String(50), default=Role.USER, nullable=False)

    hash_password = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)

    is_active = Column(BOOLEAN, default=True, nullable=False)
    is_verified = Column(BOOLEAN, default=False, nullable=False)

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
