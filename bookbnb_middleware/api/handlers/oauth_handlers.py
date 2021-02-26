import requests
import json

from bookbnb_middleware.constants import OAUTH_URL, PAYMENTS_URL

headers = {"content-type": "application/json"}


def login(params):
    r = requests.get(OAUTH_URL + "/user", params=params)
    if r.status_code != 200:

        wallet_req = requests.post(PAYMENTS_URL + "/identity")
        if wallet_req.status_code != 200:
            return {"message": "wallets service currently unavailable"}, 503

        address = wallet_req.json()["address"]
        mnemonic = wallet_req.json()["mnemonic"]

        payload = {
            "token": params["token"],
            "wallet_address": address,
            "wallet_mnemonic": mnemonic,
        }
        register_user_req = requests.post(
            OAUTH_URL + "/user", data=json.dumps(payload), headers=headers
        )
        if register_user_req.status_code != 200:
            return register_user_req.json(), register_user_req.status_code

    login_req = requests.post(OAUTH_URL + "/login", params=params)
    return login_req.json(), login_req.status_code


def logout(auth_token):
    h = headers
    h["Authorization"] = auth_token
    r = requests.post(OAUTH_URL + "/logout", headers=h)
    return r.json(), r.status_code
