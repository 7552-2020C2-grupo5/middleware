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

    # intentBookBatch

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

    transaction_hash = payments_req.json()["transaction_hash"]

    bookings_patch_payload = {
        "blockchain_transaction_hash": transaction_hash,
    }
    booking_id = bookings_post_req.json()["id"]

    requests.patch(
        BOOKINGS_URL + '/' + str(booking_id),
        data=json.dumps(bookings_patch_payload),
        headers=headers,
    )

    params = {
        "blockchain_transaction_hash": transaction_hash,
        "blockchain_status": "PENDING",
    }
    while True:
        r = requests.get(BOOKINGS_URL, params=params)
        if len(r.json()) > 0:
            break
        time.sleep(1)

    # acceptBatch

    tenant_address = payload["tenant_address"]
    publication_owner_id = payload["publication_owner_id"]

    get_wallet_req = requests.get(USERS_URL + '/wallet/' + str(publication_owner_id))
    mnemonic = get_wallet_req.json()["mnemonic"]

    accept_booking_payload = {
        "roomOwnerMnemonic": mnemonic,
        "bookerAddress": tenant_address,
        "blockchainId": payload["blockchain_id"],
        "initialDate": payload["initial_date"],
        "finalDate": payload["final_date"],
        "bookingId": booking_id,
    }

    accept_req = requests.post(
        PAYMENTS_URL + '/bookings/accept',
        data=json.dumps(accept_booking_payload),
        headers=headers,
    )

    if accept_req.status_code == 500:
        return accept_req.json(), accept_req.status_code

    # owner_scheduled_notif_payload = {
    #    "to": ,
    #    "type": "hostReview",
    #    "at":
    # }

    # booker_scheduled_notif_payload = {
    #    "type": "publicationReview"
    # }

    return bookings_post_req.json(), bookings_post_req.status_code
