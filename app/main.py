from fastapi import FastAPI
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.middleware import register_middleware , LoggingMiddleware
from app.core.logging import logger
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
    AppExceptionHandler,
    global_exception
)


@app.get("/")
def home():
    return {
        "app": settings.APP_NAME,
        "debug": settings.DEBUG
    }

@app.get("/health")
async def  health():
    return {'message':"this is active and running"}