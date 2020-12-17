import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.bookbnb.users_handlers import (
    login_user,
    create_user,
    list_users,
    get_user,
)
from bookbnb_middleware.api.bookbnb.parsers import (
    user_post_parser,
    user_login_model,
)
from bookbnb_middleware.api.bookbnb.serializers import (
    user_get_serializer,
    user_logged_model,
    user_error_model,
)
from bookbnb_middleware.api.api import api
from bookbnb_middleware.constants import SUCCESS_MSG

log = logging.getLogger(__name__)

ns = api.namespace("bookbnb/users", description="Operations related to bookbnb users")


@ns.route("/login")
class Login(Resource):
    @api.expect(user_login_model)
    @ns.response(code=201, model=user_logged_model, description='Success')
    @ns.response(code=401, model=user_error_model, description='Invalid credentials')
    @ns.response(code=404, model=user_error_model, description='User does not exist')
    def post(self):
        """
        Logins user
        """
        res, status_code = login_user(request.json)
        return res, status_code


@ns.route("/")
class User(Resource):
    @api.expect(user_post_parser)
    @api.doc("create_user", responses={201: SUCCESS_MSG})
    def post(self):
        """
        Creates a new user.
        """
        res, status_code = create_user(request.json)
        return res, status_code

    @api.doc("list_users")
    @api.marshal_list_with(user_get_serializer)
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
    @api.marshal_with(user_get_serializer)
    def get(self, user_id):
        """
        Get a user by id.
        """
        res, status_code = get_user(user_id)
        return res, status_code
