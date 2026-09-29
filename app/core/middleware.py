import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that measures and logs the duration of each HTTP request.
    Example log: GET /users/ 200 0.045s
    """
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round(time.time() - start_time, 3)

        logger.info(
            f"{request.method} {request.url.path} "
            f"{response.status_code} "
            f"{duration}s"
        )
        return response


def register_middleware(app: FastAPI):
    """
    Configures and attaches all global HTTP middlewares to the FastAPI instance.
    """
    # GZip compression for responses larger than 1,000 bytes
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )

    # Cross-Origin Resource Sharing (CORS) settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS.split(','),
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # Uncomment HTTPSRedirectMiddleware in production to force HTTPS redirection:
    # This will redirect all HTTP requests to HTTPS.
    # Use this only in production environments where you have an SSL certificate.
    # if settings.ENABLE_HTTPS_REDIRECT:
    #     app.add_middleware(HTTPSRedirectMiddleware)

    # Protect against Host Header Injection attacks
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS.split(','),
    )

    # Custom request timing and log middleware
    app.add_middleware(LoggingMiddleware)
