from fastapi import Depends
from app.shared.security.current_user_validation import get_current_user
from .policy import ROLE_POLICY
from .exception import RoleException


class PermissionChecker:
    """
    FastAPI dependency callable that checks if the currently authenticated user's
    assigned role holds all required permissions defined for a route.

    Raises:
        RoleException (HTTP 403 Forbidden): If any required permission is missing.
    """

    def __init__(self, permissions: list):
        self.permissions = permissions

    async def __call__(self, current_user=Depends(get_current_user)):
        # Retrieve the role string from the current authenticated user instance
        user_role = current_user.role

        # Look up allowed permissions for this role in our central ROLE_POLICY dictionary
        allowed_permissions = ROLE_POLICY.get(user_role, set())

        # Verify that all required route permissions exist within allowed permissions
        for permission in self.permissions:
            if permission not in allowed_permissions:
                raise RoleException()