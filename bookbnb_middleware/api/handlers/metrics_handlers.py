import requests

from bookbnb_middleware.constants import (
    USERS_METRICS_URL,
    BOOKINGS_METRICS_URL,
    PUBLICATIONS_METRICS_URL,
)

from bookbnb_middleware.utils import get_sv_auth_headers


def get_all_metrics(params):
    h = get_sv_auth_headers()
    bookings_metrics_req = requests.get(BOOKINGS_METRICS_URL, params=params, headers=h)
    users_metrics_req = requests.get(USERS_METRICS_URL, params=params, headers=h)
    publications_metrics_req = requests.get(
        PUBLICATIONS_METRICS_URL, params=params, headers=h
    )
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
