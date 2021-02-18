from flask_restx import fields, reqparse
from bookbnb_middleware.api.api import api
from bookbnb_middleware.api.models.questions_models import publication_question_model

publication_image_model = api.model(
    "Publication Image Model",
    {
        "url": fields.String(required=True, description="URL location for the image"),
        "id": fields.String(readonly=True, description="UUID for this image"),
    },
)

loc_model = api.model(
    "Location Model",
    {
        "latitude": fields.Float(description="latitude", required=True),
        "longitude": fields.Float(description="longitude", required=True),
    },
)

base_publication_model = api.model(
    'Base Publication Model',
    {
        "id": fields.Integer(
            readonly=True, description="The unique identifier of the publication"
        ),
        "user_id": fields.Integer(description="Id of owner user"),
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
        "images": fields.List(
            fields.Nested(publication_image_model),
            required=True,
            description="List of images URLs",
        ),
    },
)

new_publication_model = api.inherit(
    "New Publication Model",
    base_publication_model,
    {
        "loc": fields.Nested(
            loc_model,
            required=True,
            description="Location of the rental place",
        ),
        "mnemonic": fields.String(
            required=True, description="Mnemonic of the user wallet"
        ),
    },
)

publication_model = api.inherit(
    'Created Publication Model',
    base_publication_model,
    {
        "loc": fields.Nested(loc_model),
        "publication_date": fields.DateTime(description="Date of the publication"),
        "questions": fields.List(
            fields.Nested(publication_question_model),
            description="Questions regarding the publication",
        ),
    },
)

filter_model = reqparse.RequestParser()
filter_model.add_argument(
    "bathrooms",
    type=int,
    help="minimum amount of bathrooms needed",
    store_missing=False,
)
filter_model.add_argument(
    "rooms",
    type=int,
    help="Minimum amount of rooms needed",
    store_missing=False,
)
filter_model.add_argument(
    "beds",
    type=int,
    help="Minimum amount of beds needed",
    store_missing=False,
)
filter_model.add_argument(
    "price_per_night",
    type=int,
    help="Max price per night",
    store_missing=False,
)
filter_model.add_argument(
    "user_id",
    type=int,
    help="id of owner user",
    store_missing=False,
)
filter_model.add_argument(
    "latitude",
    type=float,
    help="The latitude for the point near to look for.\
         Note: max_distance and longitude are required when using latitude.",
    store_missing=True,
)
filter_model.add_argument(
    "longitude",
    type=float,
    help="The longitude for the point near to look for.\
        Note: max_distance and latitude are required when using longitude.",
    store_missing=True,
)
filter_model.add_argument(
    "max_distance",
    type=float,
    help="The maximum distance (in km.) for the point near to look for.\
         Note: latitude and longitude are required when using max_distance.",
    store_missing=True,
)
filter_model.add_argument(
    "initial_date",
    type=str,
    help="If not final date present it will filter\
         publications available after initial_date.\
         Note: if both initial_date and final_date present,\
         it will filter all publications available between\
         initial_date and final_date.",
    store_missing=True,
)
filter_model.add_argument(
    "final_date",
    type=str,
    help="If not initial_date present it will filter\
         all publications available before final_date.\
         Note: if both initial_date and final_date present,\
         it will filter all publications available between\
         initial_date and final_date.",
    store_missing=True,
)

error_model = api.model(
    "Publications error model",
    {"message": fields.String(description="A message describing the error")},
)
