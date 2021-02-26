import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.users_handlers import (edit_user_profile,
                                                            get_user_profile,
                                                            list_users, login,
                                                            logout, register,
                                                            reset_password)
from bookbnb_middleware.api.models.users_models import (auth_model, edit_model,
                                                        email_model,
                                                        error_model,
                                                        logged_model,
                                                        logged_out_model,
                                                        login_model,
                                                        profile_model,
                                                        register_model,
                                                        registered_model,
                                                        success_model)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Users",
    path="/bookbnb/users",
    description="Operations related to bookbnb users",
)


@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model)
    @ns.response(code=201, model=logged_model, description="Success")
    @ns.response(code=401, model=error_model, description="Invalid credentials")
    @ns.response(code=404, model=error_model, description="User does not exist")
    def post(self):
        """
        Logins user
        """
        res, status_code = login(request.json)
        return res, status_code


@ns.route("/logout")
class Logout(Resource):
    @ns.expect(auth_model)
    @ns.response(code=201, model=logged_out_model, description="Success")
    @ns.response(code=401, model=error_model, description="Token invalid or malformed")
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
    @ns.expect(register_model)
    @ns.response(code=201, model=registered_model, description="Success")
    @ns.response(code=409, model=error_model, description="User already registered")
    @ns.response(code=503, description="Service currently unavailable")
    def post(self):
        """
        Creates a new user.
        """
        res, status_code = register(request.json)
        return res, status_code

    @ns.marshal_list_with(profile_model)
    def get(self):
        """
        List all users.
        """
        res, status_code = list_users()
        return res, status_code


@ns.route("/reset_password")
class ResetPasswordResource(Resource):
    @ns.expect(email_model)
    @ns.response(code=201, model=success_model, description="Success")
    @ns.response(code=403, model=error_model, description="User is blocked")
    @ns.response(code=404, model=error_model, description="User not found")
    def post(self):
        """
        Resets user password and sends email with the new password.
        """
        res, status_code = reset_password(request.json)
        return res, status_code


@ns.route("/<int:user_id>")
@ns.param("user_id", "The user unique identifier")
@ns.response(code=200, model=profile_model, description="Success")
@ns.response(code=404, model=error_model, description="User not found")
class UserById(Resource):
    def get(self, user_id):
        """
        Get a user by id.
        """
        res, status_code = get_user_profile(user_id)
        return res, status_code

    @ns.expect(edit_model)
    def put(self, user_id):
        """
        Replace a user by id.
        """
        res, status_code = edit_user_profile(user_id, request.json)
        return res, status_code
