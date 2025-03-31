"""
Development settings for the finance tracker project.
"""

import logging

from finance_tracker.settings.custom import *
from finance_tracker.settings.django import *

if DEBUG:
    # configure docs and openapi
    INSTALLED_APPS.extend(("drf_spectacular",))

    REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
    SPECTACULAR_SETTINGS = {
        "TITLE": "Finance tracker API",
        "DESCRIPTION": "API for finance tracker project",
        "VERSION": "1.0.0",
        "SERVE_INCLUDE_SCHEMA": False,
    }

    # configure profilers if enabled
    if PROFILERS_ENABLED:
        profilers_apps = ("nplusone.ext.django", "silk")
        profilers_middlewares = (
            "nplusone.ext.django.NPlusOneMiddleware",
            "silk.middleware.SilkyMiddleware",
        )
        INSTALLED_APPS.extend(profilers_apps)
        MIDDLEWARE.extend(profilers_middlewares)

        NPLUSONE_LOGGER = logging.getLogger("nplusone")
        NPLUSONE_LOG_LEVEL = logging.INFO
