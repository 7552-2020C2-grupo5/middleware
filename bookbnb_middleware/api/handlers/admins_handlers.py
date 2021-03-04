import json
import requests

from bookbnb_middleware.constants import ADMINS_URL
from bookbnb_middleware.utils import get_sv_auth_headers

headers = {"content-type": "application/json"}


def login(payload):
    h = get_sv_auth_headers()
    h.update(headers)
    login_req = requests.post(
        ADMINS_URL + '/login', data=json.dumps(payload), headers=h
    )
    return login_req.json(), login_req.status_code


def logout(auth_token):
    h = headers
    h["Authorization"] = auth_token
    h.update(get_sv_auth_headers())
    r = requests.post(ADMINS_URL + '/logout', headers=h)
    return r.json(), r.status_code


def register(payload):
    h = get_sv_auth_headers()
    h.update(headers)
    r = requests.post(ADMINS_URL, data=json.dumps(payload), headers=h)
    return r.json(), r.status_code


def list_admins(params):
    h = get_sv_auth_headers()
    r = requests.get(ADMINS_URL, params=params, headers=h)
    return r.json(), r.status_code


def get_admin_profile(admin_id):
    h = get_sv_auth_headers()
    admin_profile_req = requests.get(ADMINS_URL + "/" + str(admin_id), headers=h)
    return admin_profile_req.json(), admin_profile_req.status_code


def edit_admin_profile(admin_id, payload):
    h = get_sv_auth_headers()
    h.update(headers)
    r = requests.put(
        ADMINS_URL + "/" + str(admin_id), data=json.dumps(payload), headers=h
    )
    return r.json(), r.status_code
