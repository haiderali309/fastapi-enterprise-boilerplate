from app.core.exception_handlers import AppExceptionHandler
from fastapi import status


class EmailAlreadyExistsException(AppExceptionHandler):

    def __init__( self, email: str ):

        super().__init__(

            message=f"Email {email} already exists",

            status_code=status.HTTP_409_CONFLICT,
        )

class EmailDoesNotExistException(AppExceptionHandler):

    def __init__( self, email: str):

        super().__init__(

            message=f"Email {email} does not exists",

            status_code=status.HTTP_404_NOT_FOUND,
        )

class PasswordException(AppExceptionHandler):

    def __init__( self, password : str ):

        super().__init__(

            message=f"Password not match the formate. {password}",

            status_code=status.HTTP_400_BAD_REQUEST,
        )

class PasswordNotMatchException(AppExceptionHandler):

    def __init__( self, email: str , password : str ):

        super().__init__(

            message=f"Password {password} not match to your Email {email}",

            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class UserNameException(AppExceptionHandler):

    def __init__( self, user_name: str ):

        super().__init__(

            message=f"User Name {user_name} already exists.",

            status_code=status.HTTP_400_BAD_REQUEST,
        )

class EmailNotVerified(AppExceptionHandler):

    def __init__( self):

        super().__init__(

            message=f"Email could not be verified. Try again",

            status_code=status.HTTP_400_BAD_REQUEST,
        )

class InvalidCredentialsException(AppExceptionHandler):

    def __init__(self):

        super().__init__(

            message="Invalid email or password",

            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class UserInactiveException(AppExceptionHandler):

    def __init__(self):

        super().__init__(

            message="User account is deactivated",

            status_code=status.HTTP_403_FORBIDDEN,
        )