import re


def password_validator(value : str):
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        if not re.search(r"[0-9]", value):
            raise ValueError(
                "Password must contain at least one number"
            )

        if not re.search(r"[@$!%*?&]", value):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return value