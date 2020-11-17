from flask_restx import fields
from bookbnb_middleware.api.api import api

user_get_serializer = api.model(
    "User get serialization",
    {
        "id": fields.Integer(description="The user unique identifier"),
        "first_name": fields.String(required=True, description="The user first name"),
        "last_name": fields.String(required=True, description="The user last name"),
        "email": fields.String(required=True, description="The user email"),
    },
)

publication_get_serializer = api.model(
    "Publication get serialization",
    {
        "id": fields.Integer(
            required=True, description="The unique identifier of the publication"
        ),
        "title": fields.String(
            required=True, description="The title of the publication."
        ),
        "description": fields.String(
            required=True, description="A description of the publication"
        ),
        "rooms": fields.Integer(
            required=True,
            description="The amount of rooms in the published rental place.",
        ),
        "beds": fields.Integer(
            required=True,
            description="The amount of beds in the published rental place",
        ),
        "bathrooms": fields.Integer(
            required=True, description="The amount of bathrooms in the rental place"
        ),
        "price_per_night": fields.Float(
            required=True, description="How much a night costs in the rental place"
        ),
    },
)
