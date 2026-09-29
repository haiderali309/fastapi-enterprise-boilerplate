from app.core.exception_handlers import AppExceptionHandler
from fastapi import status


class RoleException(AppExceptionHandler):

    def __init__(self):

        super().__init__(

            message=f"Permission denied",

            status_code=status.HTTP_403_FORBIDDEN,
        )