import requests
from bookbnb_middleware.constants import BOOKINGS_URL

headers = {"content-type": "application/json"}


def list_bookings(params):
    r = requests.get(BOOKINGS_URL, params=params)
    return r.json(), r.status_code
