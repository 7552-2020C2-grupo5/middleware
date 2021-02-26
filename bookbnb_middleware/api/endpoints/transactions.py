import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.transactions_handlers import (
    get_address, get_balance, send_transaction)
from bookbnb_middleware.api.models.transactions_models import (
    address_model, balance_model, error_model, send_transaction_model)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Transactions",
    path="/bookbnb/transactions",
    description="Operations related to bookbnb transactions",
)


@ns.route("/address/<int:user_id>")
@ns.param("user_id", "The user id")
class WalletAddressResource(Resource):
    @ns.response(code=200, model=address_model, description="Success")
    @ns.response(code=404, model=error_model, description="User not Found")
    @ns.response(code=403, model=error_model, description="User Blocked")
    def get(self, user_id):
        """
        Gets wallet address related to user id
        """
        res, status_code = get_address(user_id)
        return res, status_code


@ns.route("/<string:address>")
@ns.param("address", "The user's wallet address")
class TransactionsResource(Resource):
    @ns.response(code=200, model=balance_model, description="Success")
    @ns.response(code=400, model=error_model, description="Bad request")
    def get(self, address):
        """
        Gets balance of a wallet
        """
        res, status_code = get_balance(address)
        return res, status_code

    @ns.response(code=200, description="Success")
    @ns.response(code=400, model=error_model, description="Bad request")
    @ns.expect(send_transaction_model)
    def post(self, address):
        """
        Sends fixed ethers to a wallet
        """
        res, status_code = send_transaction(address, request.json)
        return res, status_code
