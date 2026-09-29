from app.authorization.router import (SecureRouter)
from .schemas import (
    RequestCreateUser,
    VerifyEmailRequest,
    ResendEmailVerificationRequest,
    RequestLoginUser,
    RequestForgotPassword,
    RequestResetPassword
)
from app.modules.tokens.schemas import RefreshTokenRequest
from app.shared.dependencies import DB_SESSION
from .service import (
    create_user_service,
    verify_email_service,
    resend_email_verification_service,
    login_user_service,
    refresh_token_service,
    logout_service,
    forgot_password_service,
    reset_password_service
)
from app.core.responses import APIResponse
from fastapi import status
from app.core.logging import logger

router = SecureRouter(
        prefix="/auth",
        tags=["Auth"]
        )

@router.post("/create")
async def create_user(db: DB_SESSION, request: RequestCreateUser):
    try:
        user = await create_user_service(db, request)

        return APIResponse.success(
            data=None,
            message=f"User created successfully. Please check your Email: {user.email} to verify you account",
            status_code=status.HTTP_201_CREATED,
        )

    except Exception:
        logger.exception("Error while creating user")
        raise


@router.get('/verify-email')
async def verify_user_email(db: DB_SESSION, token: VerifyEmailRequest):
    try:
        is_verified = await verify_email_service(db, token.token)

        if is_verified:
            return APIResponse.success(
                    message="Email verified successfully",
                    status_code=status.HTTP_200_OK,
                )

    except Exception:
        logger.exception("Error while verifying email")
        raise



@router.post('/resend-email-verification')
async def resend_email_verification(db: DB_SESSION, request: ResendEmailVerificationRequest):

    try:
        is_verified = await resend_email_verification_service(db, request.email)

        if is_verified:
            return APIResponse.success(
                    message="Email verified successfully",
                    status_code=status.HTTP_200_OK,
                )

    except Exception:
        logger.exception("Error while resending verification email")
        raise


@router.post('/login')
async def login(db: DB_SESSION, request: RequestLoginUser):
    try:
        tokens = await login_user_service(db, request)
        return APIResponse.success(
            data=tokens,
            message="Login successful",
            status_code=status.HTTP_200_OK
        )
    except Exception:
        logger.exception("Error during login")
        raise


@router.post('/refresh')
async def refresh_token(db: DB_SESSION, request: RefreshTokenRequest):
    try:
        tokens = await refresh_token_service(db, request.refresh_token)
        return APIResponse.success(
            data=tokens,
            message="Token refreshed successfully",
            status_code=status.HTTP_200_OK
        )
    except Exception:
        logger.exception("Error refreshing token")
        raise


@router.post('/logout')
async def logout(db: DB_SESSION, request: RefreshTokenRequest):
    try:
        await logout_service(db, request.refresh_token)
        return APIResponse.success(
            message="Logout successful",
            status_code=status.HTTP_200_OK
        )
    except Exception:
        logger.exception("Error during logout")
        raise


@router.post('/forgot-password')
async def forgot_password(db: DB_SESSION, request: RequestForgotPassword):
    try:
        await forgot_password_service(db, request.email)
        return APIResponse.success(
            message="Password reset link sent to your email",
            status_code=status.HTTP_200_OK
        )
    except Exception:
        logger.exception("Error during forgot password request")
        raise


@router.post('/reset-password')
async def reset_password(db: DB_SESSION, request: RequestResetPassword):
    try:
        await reset_password_service(db, request.token, request.new_password)
        return APIResponse.success(
            message="Password reset successful",
            status_code=status.HTTP_200_OK
        )
    except Exception:
        logger.exception("Error resetting password")
        raise


            
