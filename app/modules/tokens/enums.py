from enum import Enum


class TokenType(str, Enum):

    REFRESH = "refresh"

    EMAIL_VERIFY = "email_verify"

    PASSWORD_RESET = "password_reset"