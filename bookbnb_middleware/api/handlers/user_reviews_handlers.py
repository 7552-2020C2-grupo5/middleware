import json

import requests

from bookbnb_middleware.constants import USER_REVIEWS_URL

headers = {"content-type": "application/json"}


def list_user_reviews(params):
    r = requests.get(USER_REVIEWS_URL + "/reviews", params=params)
    return r.json(), r.status_code


def create_user_review(payload):
    r = requests.post(
        USER_REVIEWS_URL + "/reviews", data=json.dumps(payload), headers=headers
    )
    return r.json(), r.status_code


def get_reviewee_score(reviewee_id):
    r = requests.get(USER_REVIEWS_URL + "/score/user/" + str(reviewee_id))
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code
