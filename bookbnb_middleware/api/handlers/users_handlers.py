import base64
import json
import os
import requests

from bookbnb_middleware.api.handlers.transactions_handlers import (
    get_address,
    get_balance,
)

from bookbnb_middleware.constants import (
    NOTIFICATIONS_URL,
    PAYMENTS_URL,
    USERS_URL,
    BOOKBNB_TOKEN,
)

headers = {"content-type": "application/json"}


def login(payload):

    login_payload = {"email": payload["email"], "password": payload["password"]}
    login_req = requests.post(
        USERS_URL + '/login', data=json.dumps(login_payload), headers=headers
    )

    if login_req.status_code != 201:
        return login_req.json(), login_req.status_code

    token = login_req.json()["token"]
    s = token.split(".")[1]

    bin_data = base64.urlsafe_b64decode(s + "=" * (4 - len(s) % 4))
    user_data = json.loads(bin_data.decode())

    push_token_payload = {
        "user_id": user_data["sub"],
        "push_token": payload["push_token"],
    }
    requests.put(
        NOTIFICATIONS_URL + "/user_token",
        data=json.dumps(push_token_payload),
        headers=headers,
    )

    return login_req.json(), login_req.status_code


def logout(auth_token):
    h = headers
    h["Authorization"] = auth_token
    r = requests.post(USERS_URL + '/logout', headers=h)
    return r.json(), r.status_code


def register(payload):
    wallet_req = requests.post(PAYMENTS_URL + "/identity")
    if wallet_req.status_code != 200:
        return None, 503

    wallet_info = wallet_req.json()
    payload["wallet_address"] = wallet_info["address"]
    payload["wallet_mnemonic"] = wallet_info["mnemonic"]

    r = requests.post(USERS_URL, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def reset_password(payload):
    r = requests.post(
        USERS_URL + "/reset_password", data=json.dumps(payload), headers=headers
    )
    return r.json(), r.status_code


def list_users(params):
    h = {"BookBNB-Authorization": os.getenv(BOOKBNB_TOKEN.upper(), "_")}
    r = requests.get(USERS_URL, params=params, headers=h)
    return r.json(), r.status_code


def get_user_data(user_id):
    url = USERS_URL + "/" + str(user_id)
    user_profile_req = requests.get(url)
    if user_profile_req.status_code != 200:
        return user_profile_req.json(), user_profile_req.status_code

    user_address_data, status_code = get_address(user_id)
    user_balance_data, status_code = get_balance(user_address_data["address"])
    if status_code != 200:
        return user_balance_data, status_code

    res = user_profile_req.json()
    res.update(user_address_data)
    res.update(user_balance_data)

    return res, 200


def edit_user_profile(user_id, payload):
    url = USERS_URL + "/" + str(user_id)
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def block_user(user_id):
    url = USERS_URL + "/" + str(user_id)
    r = requests.delete(url)
    return r.json(), r.status_code
