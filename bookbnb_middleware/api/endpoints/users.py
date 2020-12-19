import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.handlers.users_handlers import (
    login,
    logout,
    register,
    list_users,
    get_user_profile,
    edit_user_profile,
    validate_token,
)
from bookbnb_middleware.api.models.users_models import (
    register_model,
    registered_model,
    login_model,
    logged_model,
    error_model,
    profile_model,
    auth_model,
    logged_out_model,
    edit_model,
)

from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace(
    name="Users",
    path="/bookbnb/users",
    description="Operations related to bookbnb users",
)


@ns.route("/login")
class Login(Resource):
    @api.expect(login_model)
    @ns.response(code=201, model=logged_model, description='Success')
    @ns.response(code=401, model=error_model, description='Invalid credentials')
    @ns.response(code=404, model=error_model, description='User does not exist')
    def post(self):
        """
        Logins user
        """
        res, status_code = login(request.json)
        return res, status_code


@ns.route("/logout")
class Logout(Resource):
    @api.expect(auth_model)
    @ns.response(code=201, model=logged_out_model, description='Success')
    @ns.response(code=401, model=error_model, description='Token invalid or malformed')
    def post(self):
        """
        Logouts user
        """
        parser_args = auth_model.parse_args()
        auth_token = parser_args.Authorization
        res, status_code = logout(auth_token)
        return res, status_code


@ns.route("/")
class User(Resource):
    @api.expect(register_model)
    @ns.response(code=201, model=registered_model, description='Success')
    @ns.response(code=409, model=error_model, description='User already registered')
    def post(self):
        """
        Creates a new user.
        """
        res, status_code = register(request.json)
        return res, status_code

    @api.marshal_list_with(profile_model)
    def get(self):
        """
        List all users.
        """
        res, status_code = list_users()
        return res, status_code


@ns.route('/validate_token')
class UserTokenValidatorResource(Resource):
    @api.expect(auth_model)
    @api.response(code=200, description="Success")
    @api.response(code=401, model=error_model, description="Invalid token")
    @api.response(code=400, model=error_model, description="Malformed token")
    def get(self):
        parser_args = auth_model.parse_args()
        auth_token = parser_args.Authorization
        res, status_code = validate_token(auth_token)
        return res, status_code


@ns.route("/<int:user_id>")
@api.param("user_id", "The user unique identifier")
@api.response(code=200, model=profile_model, description="Success")
@api.response(code=404, model=error_model, description="User not found")
class UserById(Resource):
    def get(self, user_id):
        """
        Get a user by id.
        """
        res, status_code = get_user_profile(user_id)
        return res, status_code

    @api.expect(edit_model)
    def put(self, user_id):
        """
        Replace a user by id.
        """
        res, status_code = edit_user_profile(user_id, request.json)
        return res, status_code
