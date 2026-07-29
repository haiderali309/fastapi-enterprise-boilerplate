from app.core.exception_handlers import AppExceptionHandler



class EmailAlreadyExistsException(AppExceptionHandler):

    def __init__( self, email: str ):

        super().__init__(

            message=f"Email {email} already exists",

            status_code=409,

            error_code="EMAIL_EXISTS"
        )