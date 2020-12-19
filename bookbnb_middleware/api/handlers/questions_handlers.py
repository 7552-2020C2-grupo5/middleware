import json
import requests
from bookbnb_middleware.constants import PUBLICATIONS_URL

headers = {"content-type": "application/json"}


def create_question(publication_id, payload):
    url = PUBLICATIONS_URL + "/" + str(publication_id) + "/questions"
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code


def reply_question(publication_id, question_id, payload):
    url = (
        PUBLICATIONS_URL + "/" + str(publication_id) + "/questions/" + str(question_id)
    )
    r = requests.patch(url, data=json.dumps(payload), headers=headers)
    return r.json(), r.status_code
