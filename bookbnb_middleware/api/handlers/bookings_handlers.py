import requests
import json
from bookbnb_middleware.constants import BOOKINGS_URL, PAYMENTS_URL, USERS_URL
from datetime import datetime
import time

headers = {"content-type": "application/json"}


def list_bookings(params):
    r = requests.get(BOOKINGS_URL, params=params)
    return r.json(), r.status_code


def create_booking(payload):

    total_days = (
        datetime.fromisoformat(payload["final_date"])
        - datetime.fromisoformat(payload["initial_date"])
    ).days + 1

    total_price = total_days * payload["price_per_night"]

    booking_post_payload = {
        "tenant_id": payload["tenant_id"],
        "publication_id": payload["publication_id"],
        "total_price": total_price,
        "initial_date": payload["initial_date"],
        "final_date": payload["final_date"],
    }

    bookings_post_req = requests.post(
        BOOKINGS_URL, data=json.dumps(booking_post_payload), headers=headers
    )
    if bookings_post_req.status_code != 201:
        return bookings_post_req.json(), bookings_post_req.status_code

    intent_book_payload = {
        "mnemonic": payload["tenant_mnemonic"],
        "price": payload["price_per_night"],
        "blockchainId": payload["blockchain_id"],
        "initialDate": payload["initial_date"],
        "finalDate": payload["final_date"],
    }

    payments_req = requests.post(
        PAYMENTS_URL + '/bookings',
        data=json.dumps(intent_book_payload),
        headers=headers,
    )

    if payments_req.status_code == 500:
        return payments_req.json(), 400

    bookings_patch_payload = {
        "blockchain_transaction_hash": payments_req.json()["transaction_hash"],
        "blockchain_status": "PENDING",
        "blockchain_id": 0,  # useless
    }
    booking_id = bookings_post_req.json()["id"]

    bookings_patch_req = requests.patch(
        BOOKINGS_URL + '/' + str(booking_id),
        data=json.dumps(bookings_patch_payload),
        headers=headers,
    )

    tenant_address = payload["tenant_address"]
    publication_owner_id = payload["publication_owner_id"]

    get_wallet_req = requests.get(USERS_URL + '/wallet/' + str(publication_owner_id))
    mnemonic = get_wallet_req.json()["mnemonic"]

    time.sleep(10)  # todo sacar esta mierda

    accept_booking_payload = {
        "roomOwnerMnemonic": mnemonic,
        "bookerAddress": tenant_address,
        "blockchainId": payload["blockchain_id"],
        "initialDate": payload["initial_date"],
        "finalDate": payload["final_date"],
        "bookingId": booking_id,
    }

    print(accept_booking_payload)

    r = requests.post(
        PAYMENTS_URL + '/bookings/accept',
        data=json.dumps(accept_booking_payload),
        headers=headers,
    )
    print(r.json())

    return bookings_patch_req.json(), bookings_patch_req.status_code
