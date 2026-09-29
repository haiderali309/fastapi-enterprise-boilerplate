from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logging import logger


class AppExceptionHandler(Exception):
    """
    Base custom exception class for all domain-specific application errors.

    Usage:
        raise AppExceptionHandler(
            message="User not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    """
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, data=None, success=False):
        self.success = success
        self.message = message
        self.status_code = status_code
        self.data = data
        super().__init__(message)


async def app_exception(request: Request, error: AppExceptionHandler):
    """
    Handles custom AppExceptionHandler exceptions and returns a formatted JSON response.
    """
    return JSONResponse(
        status_code=error.status_code,
        content={
            "success": False,
            "data": error.data,
            "message": error.message,
            "status_code": error.status_code
        }
    )


async def validation_exception(request: Request, error: RequestValidationError):
    """
    Formats Pydantic request body validation errors into readable message strings.
    """
    errors = []
    for err in error.errors():
        message = err["msg"].replace("Value error, ", "")
        errors.append(f"{err['loc'][-1]}: {message}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "data": None,
            "message": ", ".join(errors),
            "status_code": status.HTTP_400_BAD_REQUEST
        }
    )


async def global_exception(request: Request, error: Exception):
    """
    Fallback exception handler for unhandled server crashes (500 Internal Server Error).
    Logs full exception tracebacks to file/console silently.
    """
    logger.exception(
        "Unhandled exception occurred",
        exc_info=error
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "data": None,
            "message": "Internal server error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )