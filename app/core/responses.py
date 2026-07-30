from fastapi.responses import JSONResponse
from fastapi import status

class APIResponse:
    @staticmethod
    def success(
            data=None,
            message="Operation completed successfully",
            status_code=status.HTTP_200_OK
    ):
        return JSONResponse(
            status_code=status_code,
            content={
                "success":True,
                "data":data,
                "message":message,
                "status_code":status_code
            }
        )
