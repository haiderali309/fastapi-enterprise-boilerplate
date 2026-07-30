from app.core.exception_handlers import AppExceptionHandler
from fastapi import status


class EmailAlreadyExistsException(AppExceptionHandler):

    def __init__( self, email: str ):

        super().__init__(

            message=f"Email {email} already exists",

            status_code=status.HTTP_409_CONFLICT,
        )