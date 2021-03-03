import logging
import requests

from bookbnb_middleware.constants import RECOMMENDATIONS_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_latest_publications(params):
    r = requests.get(RECOMMENDATIONS_URL + '/latest', params=params)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code


def get_popular_publications(params):
    r = requests.get(RECOMMENDATIONS_URL + '/popular', params=params)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code


def get_similar_publications(params):
    r = requests.get(RECOMMENDATIONS_URL + '/publications', params=params)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code


def get_reviews_cf(params):
    r = requests.get(RECOMMENDATIONS_URL + '/reviews', params=params)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code


def get_stars_cf(params):
    r = requests.get(RECOMMENDATIONS_URL + '/stars', params=params)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code
