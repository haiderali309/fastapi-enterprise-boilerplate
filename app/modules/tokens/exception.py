from app.core.exception_handlers import AppExceptionHandler
from fastapi import status

class TokenExpired(AppExceptionHandler):

    def __init__( self):

        super().__init__(

            message=f"Token is already Expired. Please request new one",

            status_code=status.HTTP_401_UNAUTHORIZED
        )


class TokenNotExists(AppExceptionHandler):

    def __init__( self):

        super().__init__(

            message=f"Token does not exists",

            status_code=status.HTTP_401_UNAUTHORIZED
        )