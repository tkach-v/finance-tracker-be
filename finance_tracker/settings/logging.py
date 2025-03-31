LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": [],
        },
    },
    "loggers": {
        logger_name: {
            "level": "WARNING",
            "propagate": True,
        }
        for logger_name in (
            "django",
            "django.request",
            "django.db.backends",
            "django.template",
        )
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}
