import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.users_handlers import (
    login_user,
    logout_user,
    register_user,
    list_users,
    get_user,
)
from bookbnb_middleware.api.users_models import (
    register_model,
    registered_model,
    login_model,
    user_logged_model,
    error_model,
    profile_model,
    logout_model,
    logged_out_model,
)

from bookbnb_middleware.api.api import api
from bookbnb_middleware.constants import SUCCESS_MSG

log = logging.getLogger(__name__)

ns = api.namespace("bookbnb/users", description="Operations related to bookbnb users")


@ns.route("/login")
class Login(Resource):
    @api.expect(login_model)
    @ns.response(code=201, model=user_logged_model, description='Success')
    @ns.response(code=401, model=error_model, description='Invalid credentials')
    @ns.response(code=404, model=error_model, description='User does not exist')
    def post(self):
        """
        Logins user
        """
        res, status_code = login_user(request.json)
        return res, status_code


@ns.route("/logout")
class Logout(Resource):
    @api.expect(logout_model)
    @ns.response(code=201, model=logged_out_model, description='Success')
    @ns.response(code=401, model=error_model, description='Token invalid or malformed')
    def post(self):
        """
        Logouts user
        """
        res, status_code = logout_user(request.headers)
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
        res, status_code = register_user(request.json)
        return res, status_code

    @api.marshal_list_with(profile_model)
    def get(self):
        """
        List all users.
        """
        res, status_code = list_users()
        return res, status_code


@ns.route("/<int:user_id>")
@api.param("user_id", "The user unique identifier")
@api.response(200, SUCCESS_MSG)
class UserById(Resource):
    @api.doc("get_user_by_id")
    @api.marshal_with(profile_model)
    def get(self, user_id):
        """
        Get a user by id.
        """
        res, status_code = get_user(user_id)
        return res, status_code
