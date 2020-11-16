from flask_restx import fields
from bookbnb_middleware.api.api import api

user_get_model = api.model(
    "User get",
    {
        "id": fields.Integer(description="The user unique identifier"),
        "first_name": fields.String(required=True, description='The user first name'),
        "last_name": fields.String(required=True, description='The user last name'),
        "email": fields.String(required=True, description='The user email'),
    },
)
