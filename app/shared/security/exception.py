from app.core.exception_handlers import AppExceptionHandler
from fastapi import status


class UserNotFound(AppExceptionHandler):

    def __init__(self):

        super().__init__(

            message=f"User not found",

            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class UserNotActive(AppExceptionHandler):

    def __init__(self):

        super().__init__(

            message=f"User is inactive",

            status_code=status.HTTP_403_FORBIDDEN,
        )