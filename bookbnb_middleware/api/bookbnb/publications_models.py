from flask_restx import fields, reqparse
from bookbnb_middleware.api.api import api

publication_post_parser = api.model(
    "Publication post parser",
    {
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

publication_get_parser = reqparse.RequestParser()
publication_get_parser.add_argument(
    "bathrooms",
    type=int,
    help="minimum amount of bathrooms needed",
    store_missing=False,
)
publication_get_parser.add_argument(
    "rooms",
    type=int,
    help="Minimum amount of rooms needed",
    store_missing=False,
)
publication_get_parser.add_argument(
    "beds", type=int, help="Minimum amount of beds needed", store_missing=False
)
publication_get_parser.add_argument(
    "price per night",
    type=int,
    help="Max price per night",
    store_missing=False,
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
