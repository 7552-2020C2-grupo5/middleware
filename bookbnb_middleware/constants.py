from enum import Enum

USERS_URL = "https://bookbnb5-users-microservice.herokuapp.com/v1/users"
ADMINS_URL = "https://bookbnb5-users-microservice.herokuapp.com/v1/admins"
OAUTH_URL = "https://bookbnb5-users-microservice.herokuapp.com/v1/oauth"
USER_TOKEN_VALIDATOR_URL = (
    "https://bookbnb5-users-microservice.herokuapp.com/v1/users/validate_token"
)
ADMIN_TOKEN_VALIDATOR_URL = (
    "https://bookbnb5-users-microservice.herokuapp.com/v1/admins/validate_token"
)
PUBLICATIONS_URL = "https://bookbnb5-publications.herokuapp.com/v1/publications"
BOOKINGS_URL = "https://bookbnb5-bookings.herokuapp.com/v1/bookings"
PAYMENTS_URL = "https://bookbnb5-payments.herokuapp.com"
USER_REVIEWS_URL = "https://bookbnb5-reviews.herokuapp.com/v1/user_reviews"
NOTIFICATIONS_URL = "https://bookbnb5-notifications.herokuapp.com/v1"
PUBLICATION_REVIEWS_URL = (
    "https://bookbnb5-reviews.herokuapp.com/v1/publication_reviews"
)
RECOMMENDATIONS_URL = (
    "https://recommendations-microservice.herokuapp.com/v1/recommendations"
)
CRYPTOCOMPARE_URL = (
    "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR"
)
BOOKINGS_METRICS_URL = "https://bookbnb5-bookings.herokuapp.com/v1/metrics"
USERS_METRICS_URL = "https://bookbnb5-users-microservice.herokuapp.com/v1/metrics"
PUBLICATIONS_METRICS_URL = "https://bookbnb5-publications.herokuapp.com/v1/metrics"

BOOKBNB_TOKEN = "bookbnb_token"


class BlockChainStatus(Enum):
    UNSET = "UNSET"
    CONFIRMED = "CONFIRMED"
    DENIED = "DENIED"
    PENDING = "PENDING"
    ERROR = "ERROR"
