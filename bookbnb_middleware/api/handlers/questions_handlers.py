import json
import requests

from bookbnb_middleware.constants import PUBLICATIONS_URL
from bookbnb_middleware.utils import get_sv_auth_headers

headers = {"content-type": "application/json"}


def create_question(publication_id, payload):
    h = get_sv_auth_headers()
    h.update(headers)
    url = PUBLICATIONS_URL + "/" + str(publication_id) + "/questions"
    r = requests.post(url, data=json.dumps(payload), headers=h)
    return r.json(), r.status_code


def reply_question(publication_id, question_id, payload):
    h = get_sv_auth_headers()
    h.update(headers)
    url = (
        PUBLICATIONS_URL + "/" + str(publication_id) + "/questions/" + str(question_id)
    )
    r = requests.patch(url, data=json.dumps(payload), headers=h)
    return r.json(), r.status_code
