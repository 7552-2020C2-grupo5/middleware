import requests
import json
from bookbnb_middleware.constants import LOGIN_URL, USERS_URL, LOGOUT_URL

headers = {"content-type": "application/json"}


def login_user(payload):
    r = requests.post(LOGIN_URL, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def logout_user(auth_header):
    h = headers
    h["Authorization"] = auth_header["Authorization"]
    r = requests.post(LOGOUT_URL, headers=h)
    return r.json(), r.status_code


def register_user(payload):
    r = requests.post(USERS_URL, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def list_users():
    r = requests.get(USERS_URL)
    return r.json(), r.status_code


def get_user(user_id):
    url = USERS_URL + "/" + str(user_id)
    r = requests.get(url)
    return r.json()
