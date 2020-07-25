import logging
from logging.config import dictConfig

logging.getLogger("werkzeug").setLevel(logging.WARNING)

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {"format": "[%(asctime)s] %(levelname)s:%(module)s: %(message)s"}
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": logging.DEBUG,
            }
        },
        "root": {"level": logging.DEBUG, "handlers": ["default"]},
    }
)
