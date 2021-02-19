from bookbnb_middleware.api.api import api
from flask_restx import fields, reqparse
from bookbnb_middleware.constants import BlockChainStatus

new_booking_model = api.model(
    'New booking model',
    {
        "tenant_id": fields.Integer(
            required=True, description="The unique identifier of the tenant"
        ),
        "tenant_mnemonic": fields.String(
            required=True, description="The tenant wallet's mnemonic"
        ),
        "blockchain_id": fields.Integer(
            required=True, description="The blockchain id of the publication"
        ),
        "publication_id": fields.Integer(
            required=True, description="The unique identifier of the publication"
        ),
        "price_per_night": fields.Float(
            required=True,
            description="Price por night of the publication (in ETH)",
        ),
        "initial_date": fields.Date(
            required=True,
            description="The starting date of the rental",
        ),
        "final_date": fields.Date(
            required=True, description="The final date of the rental"
        ),
    },
)

booking_model = api.model(
    'Booking model',
    {
        "id": fields.Integer(
            description="The unique identifier of the booking",
        ),
        "tenant_id": fields.Integer(description="The unique identifier of the tenant"),
        "publication_id": fields.Integer(
            description="The unique identifier of the publication"
        ),
        "total_price": fields.Float(
            description="The total price of the operation",
        ),
        "initial_date": fields.Date(
            description="The starting date of the rental",
        ),
        "final_date": fields.Date(description="The final date of the rental"),
        "booking_date": fields.DateTime(
            readonly=True, description="Date the booking was created"
        ),
    },
)

error_model = api.model(
    "Bookings error model",
    {"message": fields.String(description="A message describing the error")},
)

filter_model = reqparse.RequestParser()
filter_model.add_argument(
    "tenant_id",
    type=int,
    help="id of tenant",
    store_missing=False,
)
filter_model.add_argument(
    "publication_id",
    type=int,
    help="id of publication",
    store_missing=False,
)
filter_model.add_argument(
    "initial_date",
    type=str,
    help="minimum starting date",
    store_missing=False,
)
filter_model.add_argument(
    "final_date",
    type=str,
    help="maximum final date",
    store_missing=False,
)
filter_model.add_argument(
    "booking_date",
    type=str,
    help="booking date",
    store_missing=False,
)
filter_model.add_argument(
    "blockchain_status",
    type=str,
    default=BlockChainStatus.UNSET.value,
)
filter_model.add_argument(
    "blockchain_transaction_hash",
    type=str,
    store_missing=False,
)

error_model = api.model(
    "Bookings error model",
    {"message": fields.String(description="A message describing the error")},
)

error_model = api.model(
    "Bookings error model",
    {"message": fields.String(description="A message describing the error")},
)
