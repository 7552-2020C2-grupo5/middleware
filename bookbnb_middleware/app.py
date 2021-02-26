import logging.config
import os

import requests
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

from bookbnb_middleware import settings
from bookbnb_middleware.api.api import api
from bookbnb_middleware.api.endpoints.bookings import \
    ns as bookbnb_bookings_namespace
from bookbnb_middleware.api.endpoints.notifications import \
    ns as bookbnb_notifications_namespace
from bookbnb_middleware.api.endpoints.publications import \
    ns as bookbnb_publications_namespace
from bookbnb_middleware.api.endpoints.publications_reviews import \
    ns as bookbnb_publications_reviews_namespace
from bookbnb_middleware.api.endpoints.questions import \
    ns as bookbnb_questions_namespace
from bookbnb_middleware.api.endpoints.transactions import \
    ns as bookbnb_transactions_namespace
from bookbnb_middleware.api.endpoints.users import \
    ns as bookbnb_users_namespace
from bookbnb_middleware.api.endpoints.users_reviews import \
    ns as bookbnb_users_reviews_namespace
from bookbnb_middleware.api.models.users_models import auth_model
from bookbnb_middleware.constants import TOKEN_VALIDATOR_URL
from bookbnb_middleware.settings import config
from decouple import config as config_decouple
from flask_cors import CORS

environment = config["development"]
if config_decouple("PRODUCTION", default=False):
    environment = config["production"]

logging_conf_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../logging.conf")
)
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def before_request():
    excluded_paths = [
        "/",
        "/swaggerui/favicon-32x32.png",
        "/swagger.json",
        "/bookbnb/users/",
        "/bookbnb/users/login",
    ]
    if request.path not in excluded_paths:
        parser_args = auth_model.parse_args()
        auth_token = parser_args.Authorization
        h = {"content-type": "application/json", "Authorization": auth_token}
        r = requests.get(TOKEN_VALIDATOR_URL, headers=h)
        if r.status_code != 200 and auth_token != "AUTH_FAKE":
            return r.json(), r.status_code
    return


def create_app():
    new_app = Flask(__name__)

    new_app.config.from_object(environment)
    new_app.config["SWAGGER_UI_DOC_EXPANSION"] = settings.RESTX_SWAGGER_UI_DOC_EXPANSION
    new_app.config["RESTX_VALIDATE"] = settings.RESTX_VALIDATE
    new_app.config["RESTX_MASK_SWAGGER"] = settings.RESTX_MASK_SWAGGER
    new_app.config["ERROR_404_HELP"] = settings.RESTX_ERROR_404_HELP

    api.init_app(new_app)
    api.add_namespace(bookbnb_publications_namespace)
    api.add_namespace(bookbnb_questions_namespace)
    api.add_namespace(bookbnb_transactions_namespace)
    api.add_namespace(bookbnb_bookings_namespace)
    api.add_namespace(bookbnb_users_reviews_namespace)
    api.add_namespace(bookbnb_publications_reviews_namespace)
    api.add_namespace(bookbnb_notifications_namespace)
    new_app.wsgi_app = ProxyFix(
        new_app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1
    )
    new_app.before_request(before_request)
    CORS(new_app, resources={r"/*": {"origins": "*"}})
    return new_app
