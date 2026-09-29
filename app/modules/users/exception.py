from app.core.exception_handlers import AppExceptionHandler
from fastapi import status


class UserNotFoundException(AppExceptionHandler):

    def __init__(self, user_id: int = None):
        message = f"User with ID {user_id} not found" if user_id else "User not found"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )
