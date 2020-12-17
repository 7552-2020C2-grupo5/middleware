import requests
import json
from bookbnb_middleware.constants import LOGIN_URL, USER_URL

headers = {"content-type": "application/json"}


def login_user(payload):
    r = requests.post(LOGIN_URL, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def create_user(payload):
    # todo validate errors
    requests.post(USER_URL, data=json.dumps(payload), headers=headers)


def list_users():
    r = requests.get(USER_URL)
    return r.json()


def get_user(user_id):
    url = USER_URL + "/" + str(user_id)
    r = requests.get(url)
    return r.json()
