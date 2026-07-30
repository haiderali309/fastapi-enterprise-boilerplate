from fastapi import FastAPI ,status
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.middleware import register_middleware , LoggingMiddleware
from app.core.logging import logger
from app.modules.auth.exception import EmailAlreadyExistsException
from app.core.responses import APIResponse
from app.core.exception_handlers import (
    AppExceptionHandler,
    app_exception,
    global_exception)

app=FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

register_middleware(app)

app.add_exception_handler(
    AppExceptionHandler,
    app_exception
)

app.add_exception_handler(
    Exception,
    global_exception
)


@app.get("/global-error")
def global_error():
    x = 10 / 0
    return x

@app.get("/app-error")
async def app_error():
    email="haider@mail.com"
    logger.error(f'email to  wer gia {email}')
    return EmailAlreadyExistsException(email)

@app.get('/response')
async def api_response():
    return APIResponse.success(
        data={
        "app": settings.APP_NAME,
        "debug": settings.DEBUG
        },
        message="Operation completed successfully",
        status_code=status.HTTP_208_ALREADY_REPORTED
    )