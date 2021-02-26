import logging

from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.oauth_handlers import login, logout
from bookbnb_middleware.api.models.oauth_models import (
    oauth_token_parser,
    oauth_parser,
    error_model,
)

log = logging.getLogger(__name__)

ns = Namespace(
    name="OAuth",
    path="/bookbnb/oauth",
    description="Operations related to BookBNB OAuth",
)

ns.models[error_model.name] = error_model


@ns.route("/login")
class OAuthLogin(Resource):
    @ns.doc('oauth_login')
    @ns.expect(oauth_token_parser)
    @ns.response(code=201, description="Success")
    @ns.response(code=401, model=error_model, description="Invalid credentials")
    @ns.response(
        code=503, model=error_model, description="Service currently unavailable"
    )
    def post(self):
        """
        OAuth Login
        """
        res, status_code = login(oauth_token_parser.parse_args())
        return res, status_code


@ns.route("/logout")
class OAuthLogout(Resource):
    @ns.doc('oauth_logout')
    @ns.expect(oauth_parser)
    @ns.response(code=201, description="Success")
    @ns.response(code=401, model=error_model, description="Token invalid or malformed")
    def post(self):
        """
        OAuth Logout
        """
        auth_token = oauth_parser.parse_args().Authorization
        res, status_code = logout(auth_token)
        return res, status_code
