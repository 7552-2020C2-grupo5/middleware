from flask_restx import fields, Model

instant_notification_model = Model(
    "Instant notification model",
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
