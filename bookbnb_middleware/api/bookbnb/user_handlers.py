import requests
import json
from bookbnb_middleware.constants import USER_URL

headers = {"content-type": "application/json"}


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
