from .repository import (
    check_user_email,
    check_user_username,
    verify_user_email,
    save_user,
    get_user_by_id,
    update_user_password
)
from app.shared.password_encryption import hash_password, verify_password
from app.modules.tokens.service import (
    create_email_verify_token,
    get_token_service,
    revoke_token_service,
    create_refresh_token,
    create_password_reset_token
)
from app.shared.security.hashing import hash_token
from app.shared.security.jwt import create_access_token
from app.core.config import settings
from app.core.logging import logger
from fastapi import status
from app.modules.tokens.enums import TokenType
from app.infrastructure.email.service import send_mail
from .exception import (
    EmailAlreadyExistsException,
    UserNameException,
    EmailDoesNotExistException,
    EmailNotVerified,
    InvalidCredentialsException,
    UserInactiveException
)
from app.modules.users.models import Users


async def create_user_service(db, request_data):

    check_email = await check_user_email(db, request_data.email)

    check_username = await check_user_username(db, request_data.username)

    if check_email:
        raise EmailAlreadyExistsException(request_data.email)

    if check_username:
        raise UserNameException(request_data.username)

    user = Users(
        first_name=request_data.first_name,
        last_name=request_data.last_name,
        username=request_data.username,
        email=request_data.email,
        role=request_data.role,
        hash_password=hash_password(request_data.password),
        phone_number=request_data.phone_number
    )

    saved_user = await save_user(db, user)

    email_verification_token = await create_email_verify_token(db, saved_user.id)
    verification_link = f"{settings.FRONTEND_URL}/verify-email?token={email_verification_token}"

    try:
        await send_mail(
            subject="Account Verification Email",
            message=f"For account verification. Please click this link: {verification_link}",
            recipient_list=[saved_user.email],
            template_name="email_verification.html",
            context={
                "first_name": saved_user.first_name,
                "last_name": saved_user.last_name,
                "verification_link": verification_link,
            },
        )
    except Exception:
        logger.exception("Failed to send verification email")

    return saved_user


async def verify_email_service(db, request_token):
    token_hash = hash_token(request_token)
    token_type = TokenType.EMAIL_VERIFY

    try:
        token = await get_token_service(db, token_hash, token_type)

        is_verified = await verify_user_email(db, token.user_id)

        if is_verified:
            await revoke_token_service(db, token.id)
            return is_verified

    except Exception:
        logger.exception("Failed to verify email")
        raise


async def resend_email_verification_service(db, email):

    check_user = await check_user_email(db, email)

    if not check_user:
        raise EmailDoesNotExistException(email)

    email_verification_token = await create_email_verify_token(db, check_user.id)
    verification_link = f"{settings.FRONTEND_URL}/verify-email?token={email_verification_token}"

    try:
        await send_mail(
            subject="Account Verification Email",
            message=f"For account verification. Please click this link: {verification_link}",
            recipient_list=[check_user.email],
            template_name="email_verification.html",
            context={
                "first_name": check_user.first_name,
                "last_name": check_user.last_name,
                "verification_link": verification_link,
            },
        )
    except Exception:
        logger.exception("Failed to send verification email")

    return check_user


async def login_user_service(db, request_data):
    user = await check_user_email(db, request_data.email)
    if not user:
        raise InvalidCredentialsException()

    if not verify_password(request_data.password, user.hash_password):
        raise InvalidCredentialsException()

    if not user.is_active:
        raise UserInactiveException()

    if not user.is_verified:
        raise EmailNotVerified()

    access_token = create_access_token(user.id,user.role)
    refresh_token = await create_refresh_token(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_token_service(db, refresh_token: str):
    token_hash = hash_token(refresh_token)
    
    token_record = await get_token_service(db, token_hash, TokenType.REFRESH)

    user = await get_user_by_id(db, token_record.user_id)
    if not user:
        raise InvalidCredentialsException()

    if not user.is_active:
        raise UserInactiveException()

    await revoke_token_service(db, token_record.id)

    new_access_token = create_access_token(user.id)
    new_refresh_token = await create_refresh_token(db, user.id)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


async def logout_service(db, refresh_token: str):
    token_hash = hash_token(refresh_token)
    try:
        token_record = await get_token_service(db, token_hash, TokenType.REFRESH)
        await revoke_token_service(db, token_record.id)
        return True
    except Exception:
        return False


async def forgot_password_service(db, email: str):
    user = await check_user_email(db, email)
    if not user:
        raise EmailDoesNotExistException(email)

    reset_token = await create_password_reset_token(db, user.id)
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

    try:
        await send_mail(
            subject="Password Reset Request",
            message=f"Please click this link to reset your password: {reset_link}",
            recipient_list=[user.email],
            template_name="password_reset.html",
            context={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "reset_link": reset_link
            }
        )
    except Exception:
        logger.exception("Failed to send password reset email")
        raise

    return True


async def reset_password_service(db, token: str, new_password: str):
    token_hash = hash_token(token)
    
    token_record = await get_token_service(db, token_hash, TokenType.PASSWORD_RESET)

    hashed_pwd = hash_password(new_password)
    await update_user_password(db, token_record.user_id, hashed_pwd)
    await revoke_token_service(db, token_record.id)

    return True