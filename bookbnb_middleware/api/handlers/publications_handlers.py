from datetime import datetime
import json

import requests

from bookbnb_middleware.constants import BOOKINGS_URL, PAYMENTS_URL, PUBLICATIONS_URL

headers = {"content-type": "application/json"}


def create_publication(payload):

    if payload["price_per_night"] <= 0:
        return {"message": "Price must be greater than 0"}, 400

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
        PAYMENTS_URL + "/room", data=json.dumps(d), headers=headers
    )
    if payments_req.status_code == 500:
        requests.delete(PUBLICATIONS_URL + "/" + str(publication_id))
        return payments_req.json(), 400

    patch_payload = {
        "blockchain_transaction_hash": payments_req.json()["transaction_hash"]
    }
    r = requests.patch(
        PUBLICATIONS_URL + "/" + str(publication_id),
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
    if r.status_code != 200:
        return r.json(), r.status_code

    params = {"publication_id": publication_id, "blockchain_status": "CONFIRMED"}
    bookings = requests.get(BOOKINGS_URL, params=params).json()
    bookings_dates = []
    for booking in bookings:
        booking_date = {
            "initial_date": booking["initial_date"],
            "final_date": booking["final_date"],
        }
        bookings_dates.append(booking_date)

    resp = r.json()
    resp["bookings_dates"] = bookings_dates

    return resp, r.status_code


def replace_publication(publication_id, payload):
    if payload["price_per_night"] <= 0:
        return {"message": "Price must be greater than 0"}, 400

    resp, status_code = get_publication(publication_id)
    if status_code != 200:
        return resp, status_code

    mnemonic = payload["mnemonic"]
    old_price_per_night = resp["price_per_night"]
    blockchain_id = resp["blockchain_id"]
    if old_price_per_night != payload["price_per_night"]:
        # interaction with smart contract
        d = {
            "mnemonic": mnemonic,
            "newPrice": payload["price_per_night"],
            "roomId": blockchain_id,
        }
        payments_req = requests.patch(
            PAYMENTS_URL + "/room", data=json.dumps(d), headers=headers
        )
        if payments_req.status_code == 500:
            return payments_req.json(), 400

    payload.pop("mnemonic")
    url = PUBLICATIONS_URL + "/" + str(publication_id)
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def block_publication(publication_id):
    url = PUBLICATIONS_URL + "/" + str(publication_id)
    r = requests.delete(url)
    return r.json(), r.status_code


def star_publication(params, publication_id):
    url = PUBLICATIONS_URL + "/" + str(publication_id) + "/star"
    r = requests.post(url, params=params)
    return r.json(), r.status_code


def unstar_publication(params, publication_id):
    url = PUBLICATIONS_URL + "/" + str(publication_id) + "/star"
    r = requests.delete(url, params=params)
    return r.json(), r.status_code


def get_starrings(params, publication_id):
    url = PUBLICATIONS_URL + "/" + str(publication_id) + "/star"
    r = requests.get(url, params=params)
    return r.json(), r.status_code
