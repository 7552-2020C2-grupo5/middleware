from enum import Enum

# Microservices URIs
LOGIN_URL = "https://bookbnb5-users-microservice.herokuapp.com/v1/users/login"
LOGOUT_URL = "https://bookbnb5-users-microservice.herokuapp.com/v1/users/logout"
USERS_URL = "https://bookbnb5-users-microservice.herokuapp.com/v1/users"
TOKEN_VALIDATOR_URL = (
    "https://bookbnb5-users-microservice.herokuapp.com/v1/users/validate_token"
)
PUBLICATIONS_URL = "https://bookbnb5-publications.herokuapp.com/v1/publications"
BOOKINGS_URL = "https://bookbnb5-bookings.herokuapp.com/v1/bookings"
PAYMENTS_URL = "https://bookbnb5-payments.herokuapp.com"
USER_REVIEWS_URL = "https://bookbnb5-reviews.herokuapp.com/v1/user_reviews"
CRYPTOCOMPARE_URL = (
    "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR"
)


class BlockChainStatus(Enum):
    UNSET = "UNSET"
    CONFIRMED = "CONFIRMED"
    DENIED = "DENIED"
    PENDING = "PENDING"
    ERROR = "ERROR"
