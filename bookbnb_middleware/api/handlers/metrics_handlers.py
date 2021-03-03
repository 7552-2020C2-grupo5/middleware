import requests

from bookbnb_middleware.constants import (
    USERS_METRICS_URL,
    BOOKINGS_METRICS_URL,
    PUBLICATIONS_METRICS_URL,
)

headers = {"content-type": "application/json"}


def get_all_metrics(params):
    bookings_metrics_req = requests.get(BOOKINGS_METRICS_URL, params=params)
    users_metrics_req = requests.get(USERS_METRICS_URL, params=params)
    publications_metrics_req = requests.get(PUBLICATIONS_METRICS_URL, params=params)
    if (
        bookings_metrics_req.status_code != 200
        or bookings_metrics_req.status_code != 200
        or publications_metrics_req.status_code != 200
    ):
        return {"message": "Error occurred while fetching metrics"}, 400

    res = (
        bookings_metrics_req.json()
        + users_metrics_req.json()
        + publications_metrics_req.json()
    )
    return res, 200
