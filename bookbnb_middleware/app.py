import logging.config

import os
from flask import Flask, Blueprint
from bookbnb_middleware import settings
from bookbnb_middleware.api.bookbnb.endpoints.users import ns as bookbnb_users_namespace
from bookbnb_middleware.api.api import api

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTX_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTX_VALIDATE'] = settings.RESTX_VALIDATE
    flask_app.config['RESTX_MASK_SWAGGER'] = settings.RESTX_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTX_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(bookbnb_users_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
