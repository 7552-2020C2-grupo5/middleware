import logging
import requests

from bookbnb_middleware.constants import RECOMMENDATIONS_URL
from bookbnb_middleware.utils import get_sv_auth_headers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_latest_publications(params):
    h = get_sv_auth_headers()
    r = requests.get(RECOMMENDATIONS_URL + '/latest', params=params, headers=h)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code


def get_popular_publications(params):
    h = get_sv_auth_headers()
    r = requests.get(RECOMMENDATIONS_URL + '/popular', params=params, headers=h)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code


def get_similar_publications(params):
    h = get_sv_auth_headers()
    r = requests.get(RECOMMENDATIONS_URL + '/publications', params=params, headers=h)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code


def get_reviews_cf(params):
    h = get_sv_auth_headers()
    r = requests.get(RECOMMENDATIONS_URL + '/reviews', params=params, headers=h)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code


def get_stars_cf(params):
    h = get_sv_auth_headers()
    r = requests.get(RECOMMENDATIONS_URL + '/stars', params=params, headers=h)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code
