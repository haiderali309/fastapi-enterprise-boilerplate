from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status
from app.core.logging import logger

class AppExceptionHandler(Exception):

    def __init__(self,message : str, status_code : int = status.HTTP_400_BAD_REQUEST, data=None, success=False):
        self.success=success
        self.message=message
        self.status_code=status_code
        self.data=data

        super().__init__(message)


async def app_exception(request:Request,error:AppExceptionHandler):
    return JSONResponse(
        status_code=error.status_code,
        content={
            "success": False,
            "data":error.data,
            "message":error.message,
            "status_code":error.status_code
        }
    )

async def global_exception(request:Request,error:Exception):
    logger.exception(
        "Unhandled exception",
        exc_info=error
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "data":None,
            "message":str(error),
            "status_code":status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        
    )