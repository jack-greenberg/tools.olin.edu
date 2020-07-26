import logging
from logging.config import dictConfig

format = "[%(asctime)s] %(levelname)s:%(module)s: %(message)s"

dictConfig(
    {
        "version": 1,
        "formatters": {"default": {"format": format}},
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": logging.INFO,
            },
            "_internal": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": logging.WARNING,
            },
        },
        "root": {"level": logging.INFO, "handlers": ["default"]},
    }
)
