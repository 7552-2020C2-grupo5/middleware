import json
import requests
from bookbnb_middleware.constants import PUBLICATIONS_URL, PAYMENTS_URL

headers = {"content-type": "application/json"}


def create_publication(payload):
    # interaction with payments microservice
    d = {"mnemonic": payload["mnemonic"], "price": payload["price_per_night"]}
    payments_req = requests.post(
        PAYMENTS_URL + '/room', data=json.dumps(d), headers=headers
    )

    if payments_req.status_code == 500:
        return payments_req.json(), 400

    # to do, get roomId given by smart contract and save on publications microservice
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
