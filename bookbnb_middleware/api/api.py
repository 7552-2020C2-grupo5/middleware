import logging

from flask_restx import Api

from bookbnb_middleware.api.endpoints.bookings import ns as bookings_namespace
from bookbnb_middleware.api.endpoints.notifications import ns as notifications_namespace
from bookbnb_middleware.api.endpoints.publications import ns as publications_namespace
from bookbnb_middleware.api.endpoints.publications_reviews import (
    ns as publications_reviews_namespace,
)
from bookbnb_middleware.api.endpoints.questions import ns as questions_namespace
from bookbnb_middleware.api.endpoints.transactions import ns as transactions_namespace
from bookbnb_middleware.api.endpoints.users import ns as users_namespace
from bookbnb_middleware.api.endpoints.users_reviews import ns as users_reviews_namespace
from bookbnb_middleware.api.endpoints.oauth import ns as oauth_namespace
from bookbnb_middleware.api.endpoints.admins import ns as admins_namespace
from bookbnb_middleware.api.endpoints.metrics import ns as metrics_namespace
from bookbnb_middleware.api.endpoints.tokens import ns as tokens_namespace
from bookbnb_middleware.api.endpoints.recommendations import (
    ns as recommendations_namespace,
)

log = logging.getLogger(__name__)

api = Api(
    version="1.0.0",
    title="BookBNB Middleware API",
    description="Middleware API for integrating BookBNB backend microservices",
)
api.add_namespace(publications_namespace)
api.add_namespace(questions_namespace)
api.add_namespace(transactions_namespace)
api.add_namespace(bookings_namespace)
api.add_namespace(users_reviews_namespace)
api.add_namespace(publications_reviews_namespace)
api.add_namespace(notifications_namespace)
api.add_namespace(users_namespace)
api.add_namespace(oauth_namespace)
api.add_namespace(admins_namespace)
api.add_namespace(metrics_namespace)
api.add_namespace(tokens_namespace)
api.add_namespace(recommendations_namespace)


@api.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occurred."
    log.exception(message)
    return {"message": message}, 500
