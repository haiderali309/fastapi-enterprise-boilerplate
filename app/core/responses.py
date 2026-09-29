from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder


class APIResponse:
    """
    Standardized API JSON response builder.
    Ensures all endpoint outputs follow a predictable dictionary structure.
    """

    @staticmethod
    def success(
        data=None,
        message: str = "Operation completed successfully",
        status_code: int = status.HTTP_200_OK
    ) -> JSONResponse:
        """
        Generates a standard HTTP success response.
        """
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder({
                "success": True,
                "data": data,
                "message": message,
                "status_code": status_code
            })
        )
