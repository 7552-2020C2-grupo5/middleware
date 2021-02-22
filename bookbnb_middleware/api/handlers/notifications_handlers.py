import json
import requests
from bookbnb_middleware.constants import NOTIFICATIONS_URL

headers = {"content-type": "application/json"}


def create_instant_notification(payload):
    url = NOTIFICATIONS_URL + "/notifications"

    notifications_payload_body = json.dumps(
        {"type": payload["type"], "origin_user_id": payload["origin_user_id"]}
    )

    notifications_payload = {
        "to": payload["destination_user_id"],
        "title": "Recibiste un mensaje",
        "body": notifications_payload_body,
    }

    r = requests.post(url, data=json.dumps(notifications_payload), headers=headers)
    return r.json(), r.status_code
