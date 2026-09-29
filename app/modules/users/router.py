from app.authorization.router import SecureRouter
from app.authorization.permissions import Permission
from app.shared.dependencies import DB_SESSION
from app.shared.security.current_user_validation import get_current_user
from app.modules.users.models import Users
from fastapi import Depends, status
from app.core.responses import APIResponse
from app.core.logging import logger
from app.modules.users.schemas import UpdateProfileSchema, AdminUpdateUserSchema
from app.modules.users.service import (
    get_profile_service,
    update_profile_service,
    get_all_users_service,
    get_user_by_id_service,
    admin_update_user_service,
    admin_delete_user_service,
)

router = SecureRouter(
    prefix="/users",
    tags=["Users"]
)

# ---------------- USER ENDPOINTS ----------------

@router.get(
    "/me",
    permissions=[Permission.UPDATE_PROFILE]
)
async def get_my_profile(current_user: Users = Depends(get_current_user)):
    """Fetch profile of currently authenticated user."""
    profile = await get_profile_service(current_user)
    return APIResponse.success(
        data=profile.model_dump(),
        message="Profile retrieved successfully",
        status_code=status.HTTP_200_OK
    )


@router.put(
    "/me",
    permissions=[Permission.UPDATE_PROFILE]
)
async def update_my_profile(
    db: DB_SESSION,
    request: UpdateProfileSchema,
    current_user: Users = Depends(get_current_user)
):
    """Update profile of currently authenticated user."""
    profile = await update_profile_service(db, current_user, request)
    return APIResponse.success(
        data=profile.model_dump(),
        message="Profile updated successfully",
        status_code=status.HTTP_200_OK
    )


# ---------------- ADMIN ENDPOINTS ----------------

@router.get(
    "/",
    permissions=[Permission.VIEW_USER]
)
async def get_all_users(db: DB_SESSION, skip: int = 0, limit: int = 100):
    """Admin endpoint: List all users."""
    users = await get_all_users_service(db, skip, limit)
    return APIResponse.success(
        data=[u.model_dump() for u in users],
        message="Users list retrieved successfully",
        status_code=status.HTTP_200_OK
    )


@router.get(
    "/{id}",
    permissions=[Permission.VIEW_USER]
)
async def get_user_by_id(db: DB_SESSION, id: int):
    """Admin endpoint: Get specific user details by ID."""
    user = await get_user_by_id_service(db, id)
    return APIResponse.success(
        data=user.model_dump(),
        message="User details retrieved successfully",
        status_code=status.HTTP_200_OK
    )


@router.put(
    "/{id}",
    permissions=[Permission.UPDATE_USER]
)
async def update_user(db: DB_SESSION, id: int, request: AdminUpdateUserSchema):
    """Admin endpoint: Update user details by ID."""
    user = await admin_update_user_service(db, id, request)
    return APIResponse.success(
        data=user.model_dump(),
        message="User updated successfully",
        status_code=status.HTTP_200_OK
    )


@router.delete(
    "/{id}",
    permissions=[Permission.DELETE_USER]
)
async def delete_user(db: DB_SESSION, id: int):
    """Admin endpoint: Delete user by ID."""
    await admin_delete_user_service(db, id)
    return APIResponse.success(
        data=None,
        message=f"User {id} deleted successfully",
        status_code=status.HTTP_200_OK
    )