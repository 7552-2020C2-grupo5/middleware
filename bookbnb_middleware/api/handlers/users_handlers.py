import requests
import json
from bookbnb_middleware.constants import (
    LOGIN_URL,
    USERS_URL,
    LOGOUT_URL,
    TOKEN_VALIDATOR_URL,
    PAYMENTS_URL,
)

headers = {"content-type": "application/json"}


def login(payload):
    r = requests.post(LOGIN_URL, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def logout(auth_token):
    h = headers
    h["Authorization"] = auth_token
    r = requests.post(LOGOUT_URL, headers=h)
    return r.json(), r.status_code


def register(payload):
    wallet_req = requests.post(PAYMENTS_URL + '/identity')
    if wallet_req.status_code != 200:
        return None, 503

    wallet_info = wallet_req.json()
    payload["wallet_address"] = wallet_info["address"]
    payload["wallet_mnemonic"] = wallet_info["mnemonic"]

    r = requests.post(USERS_URL, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def list_users():
    r = requests.get(USERS_URL)
    return r.json(), r.status_code


def validate_token(auth_token):
    h = headers
    h["Authorization"] = auth_token
    r = requests.get(TOKEN_VALIDATOR_URL, headers=h)
    return r.json(), r.status_code


def get_user_profile(user_id):
    url = USERS_URL + "/" + str(user_id)
    r = requests.get(url)
    return r.json(), r.status_code


def edit_user_profile(user_id, payload):
    url = USERS_URL + "/" + str(user_id)
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code
