from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.middleware import register_middleware
from app.core.logging import logger
from app.core.exception_handlers import (
    AppExceptionHandler,
    app_exception,
    validation_exception,
    global_exception,
)

# Import modular app routers here
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router

# -----------------------------------------------------------------------------
# FastAPI Application Setup
# -----------------------------------------------------------------------------
# We initialize our main FastAPI instance with application title, debug state,
# and lifespan lifecycle events (database connection startup/shutdown).
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# -----------------------------------------------------------------------------
# Middlewares & Exception Handlers
# -----------------------------------------------------------------------------
# Register global middlewares (CORS, GZip, Host validation, Request Logging)
register_middleware(app)

# Custom application exception handler (returns standard JSON format)
app.add_exception_handler(AppExceptionHandler, app_exception)

# Pydantic validation exception handler (cleans up request payload validation errors)
app.add_exception_handler(RequestValidationError, validation_exception)

# Fallback exception handler for unexpected 500 server crashes
app.add_exception_handler(Exception, global_exception)

# -----------------------------------------------------------------------------
# Modular Router Registration (Django-like App Routers)
# -----------------------------------------------------------------------------
# Include domain routers. Add any new module routers below.
app.include_router(auth_router)
app.include_router(users_router)
