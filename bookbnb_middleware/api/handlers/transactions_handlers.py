import requests
from bookbnb_middleware.constants import PAYMENTS_URL, CRYPTOCOMPARE_URL


def get_balance(address):
    # interaction with payments microservice
    payments_req = requests.get(PAYMENTS_URL + '/balance/' + address)

    if payments_req.status_code == 500:
        return payments_req.json(), 400

    r = requests.get(CRYPTOCOMPARE_URL)
    if r.status_code != 200:
        return r.json(), r.status_code

    balance = {}
    balance["ETH"] = float(payments_req.json()["eth"])
    balance["USD"] = r.json()["USD"] * balance["ETH"]
    balance["EUR"] = r.json()["EUR"] * balance["ETH"]

    return balance, 200
