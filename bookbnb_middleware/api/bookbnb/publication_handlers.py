import json
import requests
from bookbnb_middleware.constants import PUBLICATION_URL

headers = {"content-type": "application/json"}


def create_publication(payload):
    # todo validate errors
    requests.post(PUBLICATION_URL, data=json.dumps(payload), headers=headers)


def list_publications(params):
    r = requests.get(PUBLICATION_URL, params=params)
    return r.json()


def get_publication(publication_id):
    url = PUBLICATION_URL + "/" + str(publication_id)
    r = requests.get(url)
    return r.json()
