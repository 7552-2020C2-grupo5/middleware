import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.admins_handlers import (
    edit_admin_profile,
    get_admin_profile,
    list_admins,
    login,
    logout,
    register,
)
from bookbnb_middleware.api.models.admins_models import (
    auth_model,
    edit_model,
    email_model,
    error_model,
    logged_model,
    logged_out_model,
    login_model,
    profile_model,
    register_model,
    registered_model,
    success_model,
    admin_parser,
)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Admins",
    path="/bookbnb/admins",
    description="Operations related to bookbnb admins",
)

ns.models[edit_model.name] = edit_model
ns.models[email_model.name] = email_model
ns.models[logged_model.name] = logged_model
ns.models[logged_out_model.name] = logged_out_model
ns.models[login_model.name] = login_model
ns.models[profile_model.name] = profile_model
ns.models[register_model.name] = register_model
ns.models[registered_model.name] = registered_model
ns.models[success_model.name] = success_model
ns.models[error_model.name] = error_model


@ns.route("/login")
class AdminLoginResource(Resource):
    @ns.expect(login_model)
    @ns.response(code=201, model=logged_model, description="Success")
    @ns.response(code=401, model=error_model, description="Invalid credentials")
    def post(self):
        """
        Logins admin
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
        Logouts admin
        """
        parser_args = auth_model.parse_args()
        auth_token = parser_args.Authorization
        res, status_code = logout(auth_token)
        return res, status_code


@ns.route("/")
class Admin(Resource):
    @ns.expect(register_model)
    @ns.response(code=201, model=registered_model, description="Success")
    @ns.response(code=400, model=error_model, description="Email not valid")
    @ns.response(code=409, model=error_model, description="Admin already registered")
    def post(self):
        """
        Creates a new admin.
        """
        res, status_code = register(request.json)
        return res, status_code

    @ns.expect(admin_parser)
    @ns.marshal_list_with(profile_model)
    def get(self):
        """
        List admins that match all filters.
        """
        res, status_code = list_admins(admin_parser.parse_args())
        return res, status_code


@ns.route("/<int:admin_id>")
@ns.param("admin_id", "The admin unique identifier")
@ns.response(code=200, model=profile_model, description="Success")
@ns.response(code=404, model=error_model, description="Admin not found")
class AdminById(Resource):
    def get(self, admin_id):
        """
        Get an admin by id.
        """
        res, status_code = get_admin_profile(admin_id)
        return res, status_code

    @ns.expect(edit_model)
    def put(self, admin_id):
        """
        Replace an admin by id.
        """
        res, status_code = edit_admin_profile(admin_id, request.json)
        return res, status_code
