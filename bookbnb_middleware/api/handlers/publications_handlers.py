import json
import requests
from bookbnb_middleware.constants import PUBLICATIONS_URL, PAYMENTS_URL, BOOKINGS_URL

headers = {"content-type": "application/json"}


def create_publication(payload):
    # interaction with payments microservice
    d = {"mnemonic": payload["mnemonic"], "price": payload["price_per_night"]}
    payments_req = requests.post(
        PAYMENTS_URL + '/room', data=json.dumps(d), headers=headers
    )

    if payments_req.status_code == 500:
        return payments_req.json(), 400

    payload.pop("mnemonic")

    r = requests.post(PUBLICATIONS_URL, data=json.dumps(payload), headers=headers)
    publication_id = r.json()["id"]

    patch_payload = {
        "blockchain_transaction_hash": payments_req.json()["transaction_hash"]
    }
    r = requests.patch(
        PUBLICATIONS_URL + '/' + str(publication_id),
        data=json.dumps(patch_payload),
        headers=headers,
    )

    return r.json(), r.status_code


def list_publications(params):
    if not params["initial_date"] and not params["final_date"]:
        r = requests.get(PUBLICATIONS_URL, params=params)
        return r.json(), r.status_code

    initial_date = params["initial_date"]
    final_date = params["final_date"]

    # todo ver que blockchain status setear en params_bookings
    #  hasta que se resuelva el bug!!
    params_bookings = {
        "initial_date": initial_date,
        "final_date": final_date,
        "blockchain_status": "UNSET",
    }
    bookings = requests.get(BOOKINGS_URL, params=params_bookings).json()

    pub_ids_not_available = []
    for booking in bookings:
        publication_id = booking["publication_id"]
        if publication_id not in pub_ids_not_available:
            pub_ids_not_available.append(publication_id)

    params.pop("initial_date")
    params.pop("final_date")
    publications = requests.get(PUBLICATIONS_URL, params=params).json()

    available_publications = []
    for publication in publications:
        if publication["id"] not in pub_ids_not_available:
            available_publications.append(publication)

    return available_publications, 200


def get_publication(publication_id):
    url = PUBLICATIONS_URL + "/" + str(publication_id)
    r = requests.get(url)
    return r.json(), r.status_code


def replace_publication(publication_id, payload):
    url = PUBLICATIONS_URL + "/" + str(publication_id)
    r = requests.put(url, data=json.dumps(payload))
    return r.json(), r.status_code
