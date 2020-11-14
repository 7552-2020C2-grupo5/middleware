import logging

from flask_restx import Api
from bookbnb_middleware import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='BookBNB Middleware API',
          description='BookBNB Middleware API for integrating backend microservices')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
