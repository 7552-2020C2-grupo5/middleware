import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.handlers.transactions_handlers import (
    get_balance,
    send_transaction,
    get_address,
)
from bookbnb_middleware.api.models.transactions_models import (
    error_model,
    balance_model,
    send_transaction_model,
    address_model,
)

from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace(
    name="Transactions",
    path="/bookbnb/transactions",
    description="Operations related to bookbnb transactions",
)


@ns.route("/address/<int:user_id>")
@api.param("user_id", "The user id")
class WalletAddressResource(Resource):
    @api.response(code=200, model=address_model, description="Success")
    @api.response(code=404, model=error_model, description="User not Found")
    @api.response(code=403, model=error_model, description="User Blocked")
    def get(self, user_id):
        """
        Gets wallet address related to user id
        """
        res, status_code = get_address(user_id)
        return res, status_code


@ns.route("/<string:address>")
@api.param("address", "The user's wallet address")
class TransactionsResource(Resource):
    @api.response(code=200, model=balance_model, description="Success")
    @api.response(code=400, model=error_model, description="Bad request")
    def get(self, address):
        """
        Gets balance of a wallet
        """
        res, status_code = get_balance(address)
        return res, status_code

    @api.response(code=200, description='Success')
    @api.response(code=400, model=error_model, description='Bad request')
    @api.expect(send_transaction_model)
    def post(self, address):
        """
        Sends fixed ethers to a wallet
        """
        res, status_code = send_transaction(address, request.json)
        return res, status_code
