import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.oauth_handlers import login
from bookbnb_middleware.api.models.oauth_models import (
    error_model,
    login_model,
    oauth_token_parser
)

log = logging.getLogger(__name__)

ns = Namespace(
    name="OAuth",
    path="/bookbnb/oauth",
    description="Operations related to BookBNB OAuth",
)

ns.models[error_model.name] = error_model
ns.models[login_model.name] = login_model


@ns.route("/login")
class OAuthLogin(Resource):
    @ns.doc("oauth_login")
    @ns.expect(oauth_token_parser, login_model)
    @ns.response(code=201, description="Success")
    @ns.response(code=401, model=error_model, description="Invalid credentials")
    @ns.response(code=403, model=error_model, description="User is blocked")
    @ns.response(code=400, model=error_model, description="Token malformed")
    @ns.response(
        code=503, model=error_model, description="Service currently unavailable"
    )
    def post(self):
        """
        OAuth Login
        """
        res, status_code = login(oauth_token_parser.parse_args(), request.json)
        return res, status_code
