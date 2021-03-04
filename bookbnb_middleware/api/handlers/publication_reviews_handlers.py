import json

import requests

from bookbnb_middleware.constants import PUBLICATION_REVIEWS_URL
from bookbnb_middleware.utils import get_sv_auth_headers

headers = {"content-type": "application/json"}


def list_publications_reviews(params):
    h = get_sv_auth_headers()
    r = requests.get(PUBLICATION_REVIEWS_URL + "/reviews", params=params, headers=h)
    return r.json(), r.status_code


def create_publication_review(payload):
    h = get_sv_auth_headers()
    h.update(headers)
    r = requests.post(
        PUBLICATION_REVIEWS_URL + "/reviews", data=json.dumps(payload), headers=h
    )
    return r.json(), r.status_code


def get_publication_score(publication_id):
    h = get_sv_auth_headers()
    r = requests.get(
        PUBLICATION_REVIEWS_URL + "/score/publication/" + str(publication_id), headers=h
    )
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code
