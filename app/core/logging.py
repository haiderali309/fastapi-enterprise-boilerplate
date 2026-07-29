import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": (
                "%(asctime)s | %(levelname)-8s | "
                "%(name)s | %(filename)s:%(lineno)d | %(message)s"
            )
        },
        "simple": {
            "format": "%(levelname)s | %(message)s"
        },
    },

    "handlers": {

        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
        },

        "app_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/app.log",
            "when": "midnight",
            "backupCount": 30,
            "encoding": "utf-8",
            "formatter": "standard",
            "level": "INFO",
        },

        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/error.log",
            "when": "midnight",
            "backupCount": 30,
            "encoding": "utf-8",
            "formatter": "standard",
            "level": "ERROR",
        },
    },

    "loggers": {

        "app": {
            "handlers": [
                "console",
                "app_file",
                "error_file"
            ],
            "level": "INFO",
            "propagate": False,
        },

        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
        },

        "uvicorn.error": {
            "handlers": ["console"],
            "level": "INFO",
        },

        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("app")