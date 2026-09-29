from enum import Enum


class Role(str, Enum):
    """
    Centralized collection of system user roles.
    These match the role strings stored on the Users model.
    """
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"