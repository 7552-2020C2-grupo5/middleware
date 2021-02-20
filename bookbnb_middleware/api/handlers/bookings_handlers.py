import requests
import json
from bookbnb_middleware.constants import BOOKINGS_URL, PAYMENTS_URL
from datetime import datetime

headers = {"content-type": "application/json"}


def list_bookings(params):
    r = requests.get(BOOKINGS_URL, params=params)
    return r.json(), r.status_code


def create_booking(payload):

    d = {
        "mnemonic": payload["tenant_mnemonic"],
        "price": payload["price_per_night"],
        "blockchainId": payload["blockchain_id"],
        "initialDate": payload["initial_date"],
        "finalDate": payload["final_date"],
    }

    total_days = (
        datetime.fromisoformat(payload["final_date"])
        - datetime.fromisoformat(payload["initial_date"])
    ).days + 1

    payload["total_price"] = total_days * payload["price_per_night"]

    payload.pop("tenant_mnemonic")
    payload.pop("blockchain_id")
    payload.pop("price_per_night")

    r = requests.post(BOOKINGS_URL, data=json.dumps(payload), headers=headers)
    if r.status_code != 201:
        return r.json(), r.status_code

    payments_req = requests.post(
        PAYMENTS_URL + '/bookings', data=json.dumps(d), headers=headers
    )

    if payments_req.status_code == 500:
        return payments_req.json(), 400

    booking_id = r.json()["id"]

    patch_payload = {
        "blockchain_transaction_hash": payments_req.json()["transaction_hash"],
        "blockchain_status": "CONFIRMED",
        "blockchain_id": 0,
    }
    r = requests.patch(
        BOOKINGS_URL + '/' + str(booking_id),
        data=json.dumps(patch_payload),
        headers=headers,
    )

    return r.json(), r.status_code
