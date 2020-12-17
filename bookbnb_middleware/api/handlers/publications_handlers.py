import json
import requests
from bookbnb_middleware.constants import PUBLICATIONS_URL

headers = {"content-type": "application/json"}


def create_publication(payload):
    # todo validate errors
    requests.post(PUBLICATIONS_URL, data=json.dumps(payload), headers=headers)


def list_publications(params):
    r = requests.get(PUBLICATIONS_URL, params=params)
    return r.json()


def get_publication(publication_id):
    url = PUBLICATIONS_URL + "/" + str(publication_id)
    r = requests.get(url)
    return r.json()
