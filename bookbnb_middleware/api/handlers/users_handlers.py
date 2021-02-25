import requests
import json
import base64
from bookbnb_middleware.constants import (
    LOGIN_URL,
    USERS_URL,
    LOGOUT_URL,
    PAYMENTS_URL,
    NOTIFICATIONS_URL,
)

headers = {"content-type": "application/json"}


def login(payload):

    login_payload = {"email": payload["email"], "password": payload["password"]}
    login_req = requests.post(
        LOGIN_URL, data=json.dumps(login_payload), headers=headers
    )

    if login_req.status_code != 201:
        return login_req.json(), login_req.status_code

    token = login_req.json()["token"]
    s = token.split('.')[1]

    bin_data = base64.urlsafe_b64decode(s + '=' * (4 - len(s) % 4))
    user_data = json.loads(bin_data.decode())

    push_token_payload = {
        "user_id": user_data["sub"],
        "push_token": payload["push_token"],
    }
    requests.put(
        NOTIFICATIONS_URL + '/user_token',
        data=json.dumps(push_token_payload),
        headers=headers,
    )

    return login_req.json(), login_req.status_code


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


def reset_password(payload):
    r = requests.post(
        USERS_URL + '/reset_password', data=json.dumps(payload), headers=headers
    )
    return r.json(), r.status_code


def list_users():
    r = requests.get(USERS_URL)
    return r.json(), r.status_code


def get_user_profile(user_id):
    url = USERS_URL + "/" + str(user_id)
    r = requests.get(url)
    return r.json(), r.status_code


def edit_user_profile(user_id, payload):
    url = USERS_URL + "/" + str(user_id)
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code
