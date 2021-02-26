import logging

from flask_restx import Api

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

log = logging.getLogger(__name__)

api = Api(
    version="1.0.1",
    title="BookBNB Middleware API",
    description="BookBNB Middleware API for integrating backend microservices",
)
api.add_namespace(bookbnb_publications_namespace)
api.add_namespace(bookbnb_questions_namespace)
api.add_namespace(bookbnb_transactions_namespace)
api.add_namespace(bookbnb_bookings_namespace)
api.add_namespace(bookbnb_users_reviews_namespace)
api.add_namespace(bookbnb_publications_reviews_namespace)
api.add_namespace(bookbnb_notifications_namespace)


@api.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occurred."
    log.exception(message)
    return {"message": message}, 500
