import logging

from flask_restx import Resource
from bookbnb_middleware.api.handlers.transactions_handlers import get_balance
from bookbnb_middleware.api.models.transactions_models import (
    error_model,
    balance_model,
)

from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace(
    name="Transactions",
    path="/bookbnb/transactions",
    description="Operations related to bookbnb transactions",
)


@ns.route("/<string:address>")
@api.param("address", "The user's wallet address")
class PublicationsResource(Resource):
    @api.response(code=200, model=balance_model, description="Success")
    @api.response(code=400, model=error_model, description="Bad request")
    def get(self, address):
        """
        Gets balance of a wallet
        """
        res, status_code = get_balance(address)
        return res, status_code
