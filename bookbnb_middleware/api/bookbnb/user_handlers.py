import requests
import json
from bookbnb_middleware.constants import USER_POST_URL, USER_GET_URL

headers = {'content-type': 'application/json'}


def create_user(payload):
    # todo validate errors
    requests.post(USER_POST_URL, data=json.dumps(payload), headers=headers)


def list_users():
    r = requests.get(USER_GET_URL)
    return r.json()


def update_user(user_id, payload):
    pass
    # name = data.get('category_id')
    # last_name = data.get('last_name')
    # mail = data.get('mail')


def delete_user(user_id):
    pass
