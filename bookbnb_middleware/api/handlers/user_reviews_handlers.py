import json

import requests

from bookbnb_middleware.constants import USER_REVIEWS_URL
from bookbnb_middleware.utils import get_sv_auth_headers

headers = {"content-type": "application/json"}


def list_user_reviews(params):
    h = get_sv_auth_headers()
    r = requests.get(USER_REVIEWS_URL + "/reviews", params=params, headers=h)
    return r.json(), r.status_code


def create_user_review(payload):
    h = get_sv_auth_headers()
    h.update(headers)
    r = requests.post(
        USER_REVIEWS_URL + "/reviews", data=json.dumps(payload), headers=h
    )
    return r.json(), r.status_code


def get_reviewee_score(reviewee_id):
    h = get_sv_auth_headers()
    r = requests.get(USER_REVIEWS_URL + "/score/user/" + str(reviewee_id), headers=h)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code
