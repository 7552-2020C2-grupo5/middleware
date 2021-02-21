from bookbnb_middleware.api.api import api
from flask_restx import fields

instant_notification_model = api.model(
    'Instant notification model',
    {
        "origin_user_id": fields.Integer(
            required=True,
            description="The origin user id",
        ),
        "destination_user_id": fields.Integer(
            required=True, description="The destination user id"
        ),
        "type": fields.String(required=True, description="The notification's type"),
    },
)
