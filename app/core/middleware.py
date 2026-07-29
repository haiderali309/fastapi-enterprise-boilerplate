from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.core.config import settings
from starlette.middleware.base import BaseHTTPMiddleware
import time
from app.core.logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        response = await call_next(request)

        duration = round(time.time() - start, 3)

        logger.info(
            f"{request.method} {request.url.path} "
            f"{response.status_code} "
            f"{duration}s"
        )

        return response
    

def register_middleware(app:FastAPI):

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS.split(','),
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # app.add_middleware(
    #     HTTPSRedirectMiddleware
    # )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS.split(','),
    )

    app.add_middleware(LoggingMiddleware)
