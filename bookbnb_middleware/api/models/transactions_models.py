from flask_restx import fields
from bookbnb_middleware.api.api import api

balance_model = api.model(
    "Balance Model",
    {
        "ETH": fields.Float(description="Balance of the wallet (in ETH)"),
        "USD": fields.Float(description="Balance of the wallet (in USD)"),
        "EUR": fields.Float(description="Balance of the wallet (in EUR)"),
    },
)

error_model = api.model(
    "Transactions error model",
    {"message": fields.String(description="A message describing the error")},
)
