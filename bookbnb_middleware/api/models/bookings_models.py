from flask_restx import Model, fields, reqparse

from bookbnb_middleware.constants import BlockChainStatus

create_intent_book_model = Model(
    "New booking model",
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

accept_booking_model = Model(
    "Accept booking model",
    {
        "tenant_id": fields.Integer(
            required=True, description="The unique identifier of the tenant"
        ),
        "owner_id": fields.Integer(
            required=True, description="The unique identifier of the publication owner"
        ),
        "booking_id": fields.Integer(
            required=True, description="The id of the booking"
        ),
        "publication_owner_mnemonic": fields.String(
            required=True, description="The tenant wallet's mnemonic"
        ),
        "blockchain_id": fields.Integer(
            required=True, description="The blockchain id of the publication"
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

reject_booking_model = Model(
    "Reject booking model",
    {
        "tenant_id": fields.Integer(
            required=True, description="The unique identifier of the tenant"
        ),
        "booking_id": fields.Integer(
            required=True, description="The id of the booking"
        ),
        "publication_owner_mnemonic": fields.String(
            required=True, description="The tenant wallet's mnemonic"
        ),
        "blockchain_id": fields.Integer(
            required=True, description="The blockchain id of the publication"
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

booking_model = Model(
    "Booking model",
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
        "blockchain_status": fields.String(
            description="The status on the blockchain",
        ),
        "blockchain_transaction_hash": fields.String(
            description="The hash of the transaction on the blockchain"
        ),
        "booking_status": fields.String(
            description="The status of the booking",
        ),
    },
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
    default=BlockChainStatus.CONFIRMED.value,
)
filter_model.add_argument(
    "blockchain_transaction_hash",
    type=str,
    store_missing=False,
)
filter_model.add_argument("booking_status", type=str, store_missing=False)

error_model = Model(
    "Bookings error model",
    {"message": fields.String(description="A message describing the error")},
)
