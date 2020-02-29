"""
isort:skip_file
"""
import sentry_sdk
from sentry_sdk import configure_scope
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask

from MathCaptcha.config import SENTRY_NAME, SENTRY_RELEASE, SENTRY_URL, prepare_logging, DevelopmentConfig

if SENTRY_NAME != "test" and SENTRY_URL:
    sentry_sdk.init(
        dsn=SENTRY_URL, integrations=[FlaskIntegration()], release=SENTRY_RELEASE, server_name=SENTRY_NAME,
    )
    with configure_scope() as scope:
        scope.set_tag("server_type", SENTRY_NAME)

prepare_logging()

application = Flask(__name__)
application.config.from_object(DevelopmentConfig)
application.url_map.strict_slashes = False

from MathCaptcha import math_captcha_solve

# Blueprints
application.register_blueprint(math_captcha_solve.urls.bp)
