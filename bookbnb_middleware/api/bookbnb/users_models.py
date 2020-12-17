from flask_restx import fields, reqparse
from bookbnb_middleware.api.api import api

user_login_model = api.model(
    "User login model",
    {
        "email": fields.String(required=True, description="Account email"),
        "password": fields.String(required=True, description="Account password"),
    },
)

user_post_parser = api.model(
    "User post parser",
    {
        "first_name": fields.String(required=True, description="User name"),
        "last_name": fields.String(required=True, description="User last name"),
        "email": fields.String(required=True, description="User mail"),
    },
)

user_logged_model = api.model(
    "User logged model", {"token": fields.String(description="The user session token")}
)

user_logout_model = reqparse.RequestParser()
user_logout_model.add_argument(
    'Authorization', type=str, location='headers', help="Access token", required=True
)

user_logged_out_model = api.model(
    "User logged out model",
    {
        "message": fields.String(description="A message describing the session status"),
        "status": fields.String(description="Session status"),
    },
)

user_error_model = api.model(
    "User error model",
    {"message": fields.String(description="A message describing the error")},
)

user_get_serializer = api.model(
    "User get serialization",
    {
        "id": fields.Integer(description="The user unique identifier"),
        "first_name": fields.String(required=True, description="The user first name"),
        "last_name": fields.String(required=True, description="The user last name"),
        "email": fields.String(required=True, description="The user email"),
    },
)
