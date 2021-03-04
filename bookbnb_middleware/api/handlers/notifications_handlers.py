import json

import requests

from bookbnb_middleware.constants import NOTIFICATIONS_URL
from bookbnb_middleware.utils import get_sv_auth_headers

headers = {"content-type": "application/json"}


def create_instant_notification(payload):
    h = get_sv_auth_headers()
    h.update(headers)
    url = NOTIFICATIONS_URL + "/notifications"

    notifications_payload_body = {
        "type": payload["type"],
        "origin_user_id": payload["origin_user_id"],
    }

    notifications_payload = {
        "to": payload["destination_user_id"],
        "title": "Nuevo mensaje",
        "body": "Clickea acá para verlo",
        "data": notifications_payload_body,
    }

    r = requests.post(url, data=json.dumps(notifications_payload), headers=h)
    return r.json(), r.status_code
