import json
import requests
from bookbnb_middleware.constants import PUBLICATIONS_URL

headers = {"content-type": "application/json"}


def create_publication(payload):
    r = requests.post(PUBLICATIONS_URL, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def list_publications(params):
    r = requests.get(PUBLICATIONS_URL, params=params)
    return r.json(), r.status_code


def get_publication(publication_id):
    url = PUBLICATIONS_URL + "/" + str(publication_id)
    r = requests.get(url)
    return r.json(), r.status_code


def replace_publication(publication_id, payload):
    url = PUBLICATIONS_URL + "/" + str(publication_id)
    r = requests.put(url, data=json.dumps(payload))
    return r.json(), r.status_code
