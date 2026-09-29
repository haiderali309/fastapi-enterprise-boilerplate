from enum import Enum


class Permission(str, Enum):
    """
    Centralized collection of system permissions.
    Add any new application permissions here as string enums.
    """
    CREATE_USER = "create_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    VIEW_USER = "view_user"
    UPDATE_PROFILE = "update_profile"