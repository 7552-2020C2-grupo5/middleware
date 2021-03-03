import logging.config
import os
from decouple import config as config_decouple
from flask import Flask, request
from flask_cors import CORS
import requests
from werkzeug.middleware.proxy_fix import ProxyFix

from bookbnb_middleware import settings
from bookbnb_middleware.api.api import api
from bookbnb_middleware.api.models.users_models import auth_model
from bookbnb_middleware.constants import (
    USER_TOKEN_VALIDATOR_URL,
    ADMIN_TOKEN_VALIDATOR_URL,
)
from bookbnb_middleware.settings import config

environment = config["development"]
if config_decouple("PRODUCTION", default=False):
    environment = config["production"]

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

AUTH_TOKEN = os.getenv("AUTH", "AUTH_FAKE")


def validate_authorization():
    excluded_paths = [
        "/",
        "/swaggerui/favicon-32x32.png",
        "/swagger.json",
        "/bookbnb/users/login",
        "/bookbnb/users/",
        "/bookbnb/token",
        "/bookbnb/admins/login",
        "/bookbnb/oauth/login",
        "/swaggerui/swagger-ui-standalone-preset.js",
        "/swaggerui/swagger-ui-standalone-preset.js",
        "/swaggerui/swagger-ui-bundle.js",
        "/swaggerui/swagger-ui.css",
        "/swaggerui/droid-sans.css",
    ]
    log.info(request.path)
    if request.path not in excluded_paths and request.method != "OPTIONS":
        parser_args = auth_model.parse_args()
        auth_token = parser_args.Authorization
        h = {"content-type": "application/json", "Authorization": auth_token}
        r_user = requests.get(USER_TOKEN_VALIDATOR_URL, headers=h)
        r_admin = requests.get(ADMIN_TOKEN_VALIDATOR_URL, headers=h)
        if (
            r_user.status_code != 200
            and r_admin.status_code != 200
            and auth_token != AUTH_TOKEN
        ):
            return r_user.json(), r_user.status_code


def create_app():
    new_app = Flask(__name__)

    new_app.config.from_object(environment)
    new_app.config["SWAGGER_UI_DOC_EXPANSION"] = settings.RESTX_SWAGGER_UI_DOC_EXPANSION
    new_app.config["RESTX_VALIDATE"] = settings.RESTX_VALIDATE
    new_app.config["RESTX_MASK_SWAGGER"] = settings.RESTX_MASK_SWAGGER
    new_app.config["ERROR_404_HELP"] = settings.RESTX_ERROR_404_HELP

    api.init_app(new_app)
    new_app.wsgi_app = ProxyFix(
        new_app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1
    )
    CORS(new_app, resources={r"/*": {"origins": "*"}})
    new_app.before_request(validate_authorization)
    return new_app
