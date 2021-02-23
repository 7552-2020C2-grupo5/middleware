import json
import requests
from bookbnb_middleware.constants import PUBLICATIONS_URL, PAYMENTS_URL, BOOKINGS_URL
from datetime import datetime

headers = {"content-type": "application/json"}


def create_publication(payload):

    mnemonic = payload["mnemonic"]

    payload.pop("mnemonic")
    r = requests.post(PUBLICATIONS_URL, data=json.dumps(payload), headers=headers)
    if r.status_code != 200:
        return r.json(), r.status_code

    publication_id = r.json()["id"]

    # interaction with payments microservice
    d = {
        "mnemonic": mnemonic,
        "price": payload["price_per_night"],
        "publicationId": publication_id,
    }
    payments_req = requests.post(
        PAYMENTS_URL + '/room', data=json.dumps(d), headers=headers
    )
    if payments_req.status_code == 500:
        return payments_req.json(), 400

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

    if (
        initial_date
        and final_date
        and datetime.fromisoformat(final_date) < datetime.fromisoformat(initial_date)
    ):
        return {"message": "final_date must be greater or equal than initial_date"}, 400

    params_bookings = {
        "initial_date": initial_date,
        "final_date": final_date,
        "blockchain_status": "CONFIRMED",
        "booking_status": "ACCEPTED",
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
