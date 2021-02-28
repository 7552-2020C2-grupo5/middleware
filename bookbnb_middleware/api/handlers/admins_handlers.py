import json
import requests

from bookbnb_middleware.constants import ADMINS_URL

headers = {"content-type": "application/json"}


def login(payload):
    login_req = requests.post(
        ADMINS_URL + '/login', data=json.dumps(payload), headers=headers
    )
    return login_req.json(), login_req.status_code


def logout(auth_token):
    h = headers
    h["Authorization"] = auth_token
    r = requests.post(ADMINS_URL + '/logout', headers=h)
    return r.json(), r.status_code


def register(payload):
    r = requests.post(ADMINS_URL, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def list_admins(params):
    r = requests.get(ADMINS_URL, params=params)
    return r.json(), r.status_code


def get_admin_profile(admin_id):
    url = ADMINS_URL + "/" + str(admin_id)
    admin_profile_req = requests.get(url)
    return admin_profile_req.json(), admin_profile_req.status_code


def edit_admin_profile(admin_id, payload):
    url = ADMINS_URL + "/" + str(admin_id)
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code
