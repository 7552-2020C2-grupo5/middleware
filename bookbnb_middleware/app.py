import logging.config

import os
from decouple import config as config_decouple
from flask import Flask
from bookbnb_middleware import settings
from bookbnb_middleware.settings import config
from bookbnb_middleware.api.bookbnb.endpoints.users import ns as bookbnb_users_namespace
from bookbnb_middleware.api.api import api

environment = config['development']
if config_decouple('PRODUCTION', default=False):
    environment = config['production']


app = Flask(__name__)
app.config.from_object(environment)
logging_conf_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../logging.conf')
)
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config[
        'SWAGGER_UI_DOC_EXPANSION'
    ] = settings.RESTX_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTX_VALIDATE'] = settings.RESTX_VALIDATE
    flask_app.config['RESTX_MASK_SWAGGER'] = settings.RESTX_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTX_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    api.init_app(app)
    api.add_namespace(bookbnb_users_namespace)


def main():
    initialize_app(app)
    app.run(threaded=True, port=5000)


if __name__ == "__main__":
    main()
