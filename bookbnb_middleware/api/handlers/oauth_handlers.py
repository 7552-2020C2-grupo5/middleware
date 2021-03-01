import requests
import json
import base64

from bookbnb_middleware.constants import OAUTH_URL, PAYMENTS_URL, NOTIFICATIONS_URL

headers = {"content-type": "application/json"}


def login(params, payload):
    r = requests.get(OAUTH_URL + "/user", params=params)
    if r.status_code != 200:

        wallet_req = requests.post(PAYMENTS_URL + "/identity")
        if wallet_req.status_code != 200:
            return {"message": "wallets service currently unavailable"}, 503

        address = wallet_req.json()["address"]
        mnemonic = wallet_req.json()["mnemonic"]

        register_payload = {
            "token": params["token"],
            "wallet_address": address,
            "wallet_mnemonic": mnemonic,
        }
        register_user_req = requests.post(
            OAUTH_URL + "/user", data=json.dumps(register_payload), headers=headers
        )
        if register_user_req.status_code != 200:
            return register_user_req.json(), register_user_req.status_code

    login_req = requests.post(OAUTH_URL + "/login", params=params)
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
