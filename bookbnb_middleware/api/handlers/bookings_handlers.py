from datetime import datetime
import json

import requests

from bookbnb_middleware.constants import (
    BOOKINGS_URL,
    PAYMENTS_URL,
    USERS_URL,
    NOTIFICATIONS_URL,
)

from bookbnb_middleware.utils import get_sv_auth_headers

headers = {"content-type": "application/json"}


def list_bookings(params):
    h = get_sv_auth_headers()
    r = requests.get(BOOKINGS_URL, params=params, headers=h)
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

    h = get_sv_auth_headers()
    h.update(headers)

    bookings_post_req = requests.post(
        BOOKINGS_URL, data=json.dumps(booking_post_payload), headers=h
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
        PAYMENTS_URL + "/bookings",
        data=json.dumps(intent_book_payload),
        headers=headers,
    )
    if create_intent_book_req.status_code == 500:
        bookings_patch_payload = {"blockchain_status": "ERROR"}
        requests.patch(
            BOOKINGS_URL + "/" + str(booking_id),
            data=json.dumps(bookings_patch_payload),
            headers=h,
        )
        return create_intent_book_req.json(), 400

    transaction_hash = create_intent_book_req.json()["transaction_hash"]

    bookings_patch_payload = {
        "blockchain_transaction_hash": transaction_hash,
    }

    r = requests.patch(
        BOOKINGS_URL + "/" + str(booking_id),
        data=json.dumps(bookings_patch_payload),
        headers=h,
    )

    return r.json(), r.status_code


def accept_booking(payload):

    tenant_id = payload["tenant_id"]
    publication_owner_mnemonic = payload["publication_owner_mnemonic"]
    booking_id = payload["booking_id"]
    owner_id = payload["owner_id"]
    final_date = payload["final_date"]

    h = get_sv_auth_headers()
    get_wallet_req = requests.get(USERS_URL + "/wallet/" + str(tenant_id), headers=h)
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
        PAYMENTS_URL + "/bookings/accept",
        data=json.dumps(accept_booking_payload),
        headers=headers,
    )

    if accept_req.status_code == 500:
        return accept_req.json(), 400

    publication_id = requests.get(
        BOOKINGS_URL + "/" + str(booking_id), headers=h
    ).json()["publication_id"]

    send_scheduled_notifications(publication_id, tenant_id, owner_id, final_date)

    return accept_req.json(), accept_req.status_code


def send_scheduled_notifications(publication_id, tenant_id, owner_id, booking_end_date):

    booking_end_date += "T00:00:00.000Z"

    url = NOTIFICATIONS_URL + "/scheduled_notifications"

    tenant_notification_data = {
        "type": "publicationReview",
        "publication_id": publication_id,
    }

    tenant_notification_body = {
        "to": tenant_id,
        "title": "Califica la publicación que reservaste",
        "body": "Clickea acá para calificarla",
        "data": tenant_notification_data,
        "at": booking_end_date,
    }

    owner_notification_data = {"type": "hostReview", "user_id": tenant_id}

    owner_notification_body = {
        "to": owner_id,
        "title": "Califica al huesped de tu publicación",
        "body": "Clickea acá para calificarlo",
        "data": owner_notification_data,
        "at": booking_end_date,
    }

    h = get_sv_auth_headers()
    h.update(headers)

    requests.post(url, data=json.dumps(tenant_notification_body), headers=h)
    requests.post(url, data=json.dumps(owner_notification_body), headers=h)


def reject_booking(payload):

    tenant_id = payload["tenant_id"]
    publication_owner_mnemonic = payload["publication_owner_mnemonic"]
    booking_id = payload["booking_id"]

    h = get_sv_auth_headers()
    get_wallet_req = requests.get(USERS_URL + "/wallet/" + str(tenant_id), headers=h)
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
        PAYMENTS_URL + "/bookings/reject",
        data=json.dumps(reject_booking_payload),
        headers=headers,
    )

    if reject_req.status_code == 500:
        return reject_req.json(), 400

    return reject_req.json(), reject_req.status_code


def get_booking_by_id(booking_id):
    h = get_sv_auth_headers()
    r = requests.get(BOOKINGS_URL + "/" + str(booking_id), headers=h)
    return r.json(), r.status_code
