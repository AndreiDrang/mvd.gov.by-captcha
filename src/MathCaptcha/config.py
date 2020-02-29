import logging.config
import os
from datetime import timedelta

from environs import Env

env = Env()

SENTRY_NAME = env.str("SENTRY_NAME", "test")
SENTRY_RELEASE = env.str("SENTRY_RELEASE", "0.1")
SENTRY_URL = env.str("SENTRY_URL", None)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
MEGABYTE = 1024 * 1024


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


def prepare_logging():
    # setup logs
    os.makedirs("logs", exist_ok=True)
    logging.config.dictConfig(LOGGING)


# fmt: off

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}},
    "handlers": {
        "stdout": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "standard"},
        "main_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "logs/main.log",
            "maxBytes": 50 * MEGABYTE,  # 50mb
            "backupCount": 10,
        },
        "math_captcha_solve": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "logs/math_captcha_solve.log",
            "maxBytes": 50 * MEGABYTE,  # 50mb
            "backupCount": 10,
        },
    },
    "loggers": {
        "MathCaptcha": {"handlers": ["stdout", "main_file"], "level": "DEBUG", "propagate": True},
        "MathCaptcha.math_captcha_solve": {"handlers": ["math_captcha_solve", "stdout"], "level": "INFO", "propagate": False,}
    },
}

# fmt: on
