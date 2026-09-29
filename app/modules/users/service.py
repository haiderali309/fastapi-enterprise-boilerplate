from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.repository import (
    get_all_users_repo,
    get_user_by_id_repo,
    update_user_repo,
    delete_user_repo,
)
from app.modules.users.exception import UserNotFoundException
from app.modules.users.schemas import UpdateProfileSchema, AdminUpdateUserSchema, UserResponseSchema
from app.modules.users.models import Users
from typing import List


async def get_profile_service(current_user: Users) -> UserResponseSchema:
    return UserResponseSchema.model_validate(current_user)


async def update_profile_service(db: AsyncSession, current_user: Users, schema: UpdateProfileSchema) -> UserResponseSchema:
    update_data = schema.model_dump(exclude_unset=True)
    updated_user = await update_user_repo(db, current_user, update_data)
    return UserResponseSchema.model_validate(updated_user)


async def get_all_users_service(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[UserResponseSchema]:
    users = await get_all_users_repo(db, skip=skip, limit=limit)
    return [UserResponseSchema.model_validate(u) for u in users]


async def get_user_by_id_service(db: AsyncSession, user_id: int) -> UserResponseSchema:
    user = await get_user_by_id_repo(db, user_id)
    if not user:
        raise UserNotFoundException(user_id)
    return UserResponseSchema.model_validate(user)


async def admin_update_user_service(db: AsyncSession, user_id: int, schema: AdminUpdateUserSchema) -> UserResponseSchema:
    user = await get_user_by_id_repo(db, user_id)
    if not user:
        raise UserNotFoundException(user_id)
    update_data = schema.model_dump(exclude_unset=True)
    updated_user = await update_user_repo(db, user, update_data)
    return UserResponseSchema.model_validate(updated_user)


async def admin_delete_user_service(db: AsyncSession, user_id: int) -> None:
    user = await get_user_by_id_repo(db, user_id)
    if not user:
        raise UserNotFoundException(user_id)
    await delete_user_repo(db, user)
