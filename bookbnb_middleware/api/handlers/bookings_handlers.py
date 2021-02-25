import requests
import json
from bookbnb_middleware.constants import BOOKINGS_URL, PAYMENTS_URL, USERS_URL
from datetime import datetime

headers = {"content-type": "application/json"}


def list_bookings(params):
    r = requests.get(BOOKINGS_URL, params=params)
    return r.json(), r.status_code


def create_intent_book(payload):

    initial_date = payload["initial_date"]
    final_date = payload["final_date"]

    if payload["price_per_night"] <= 0:
        return {"message": "price por night must be greater than zero"}, 412

    try:
        if datetime.fromisoformat(final_date) < datetime.fromisoformat(initial_date):
            return {
                "message": "final_date must be greater or equal than initial_date"
            }, 412
    except ValueError:  # initial_date or final_date is invalid
        return {"message": "either initial_date or initial_date is invalid"}

    total_days = (
        datetime.fromisoformat(final_date) - datetime.fromisoformat(initial_date)
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
        "bookingId": bookings_post_req.json()["id"],
    }

    booking_id = bookings_post_req.json()["id"]

    create_intent_book_req = requests.post(
        PAYMENTS_URL + '/bookings',
        data=json.dumps(intent_book_payload),
        headers=headers,
    )
    if create_intent_book_req.status_code == 500:
        bookings_patch_payload = {"blockchain_status": "ERROR"}
        requests.patch(
            BOOKINGS_URL + '/' + str(booking_id),
            data=json.dumps(bookings_patch_payload),
            headers=headers,
        )
        return create_intent_book_req.json(), 400

    transaction_hash = create_intent_book_req.json()["transaction_hash"]

    bookings_patch_payload = {
        "blockchain_transaction_hash": transaction_hash,
    }

    r = requests.patch(
        BOOKINGS_URL + '/' + str(booking_id),
        data=json.dumps(bookings_patch_payload),
        headers=headers,
    )

    return r.json(), r.status_code


def accept_booking(payload):

    tenant_id = payload["tenant_id"]
    publication_owner_mnemonic = payload["publication_owner_mnemonic"]
    booking_id = payload["booking_id"]

    get_wallet_req = requests.get(USERS_URL + '/wallet/' + str(tenant_id))
    tenant_address = get_wallet_req.json()["address"]

    accept_booking_payload = {
        "roomOwnerMnemonic": publication_owner_mnemonic,
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
        return accept_req.json(), 400

    # owner_scheduled_notif_payload = {
    #    "to": ,
    #    "type": "hostReview",
    #    "at":
    # }

    # booker_scheduled_notif_payload = {
    #    "type": "publicationReview"
    # }

    return accept_req.json(), accept_req.status_code


def reject_booking(payload):

    tenant_id = payload["tenant_id"]
    publication_owner_mnemonic = payload["publication_owner_mnemonic"]
    booking_id = payload["booking_id"]

    get_wallet_req = requests.get(USERS_URL + '/wallet/' + str(tenant_id))
    tenant_address = get_wallet_req.json()["address"]

    reject_booking_payload = {
        "roomOwnerMnemonic": publication_owner_mnemonic,
        "bookerAddress": tenant_address,
        "blockchainId": payload["blockchain_id"],
        "initialDate": payload["initial_date"],
        "finalDate": payload["final_date"],
        "bookingId": booking_id,
    }

    reject_req = requests.post(
        PAYMENTS_URL + '/bookings/reject',
        data=json.dumps(reject_booking_payload),
        headers=headers,
    )

    if reject_req.status_code == 500:
        return reject_req.json(), 400

    return reject_req.json(), reject_req.status_code
