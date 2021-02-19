import requests
import json
from bookbnb_middleware.constants import PUBLICATION_REVIEWS_URL

headers = {"content-type": "application/json"}


def list_publications_reviews(params):
    r = requests.get(PUBLICATION_REVIEWS_URL + '/reviews', params=params)
    return r.json(), r.status_code


def create_publication_review(payload):
    r = requests.post(
        PUBLICATION_REVIEWS_URL + '/reviews', data=json.dumps(payload), headers=headers
    )
    return r.json(), r.status_code


def get_publication_score(publication_id):
    r = requests.get(
        PUBLICATION_REVIEWS_URL + '/score/publication/' + str(publication_id)
    )
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), r.status_code
