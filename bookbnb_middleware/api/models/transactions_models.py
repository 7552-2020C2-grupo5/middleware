from flask_restx import fields, Model

address_model = Model(
    "User Wallet Address Model",
    {"address": fields.String(description="The wallet address")},
)

balance_model = Model(
    "Balance Model",
    {
        "ETH": fields.Float(description="Balance of the wallet (in ETH)"),
        "USD": fields.Float(description="Balance of the wallet (in USD)"),
        "EUR": fields.Float(description="Balance of the wallet (in EUR)"),
    },
)

send_transaction_model = Model(
    "Send Transaction Model",
    {
        "mnemonic": fields.String(description="The wallet mnemonic of the sender"),
        "value": fields.Float(description="Transaction value (in ETH)"),
    },
)

error_model = Model(
    "Transactions error model",
    {"message": fields.String(description="A message describing the error")},
)
