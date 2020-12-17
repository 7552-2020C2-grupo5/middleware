from flask_restx import fields, reqparse, Model
from bookbnb_middleware.api.api import api


login_model = api.model(
    "User login model",
    {
        "email": fields.String(required=True, description="Account email"),
        "password": fields.String(required=True, description="Account password"),
    },
)


logged_model = api.model(
    "User logged model", {"token": fields.String(description="The user session token")}
)


auth_model = reqparse.RequestParser()
auth_model.add_argument(
    'Authorization', type=str, location='headers', help="Access token", required=True
)


logged_out_model = api.model(
    "User logged out model",
    {
        "message": fields.String(description="A message describing the session status"),
        "status": fields.String(description="Session status"),
    },
)


error_model = api.model(
    "User error model",
    {"message": fields.String(description="A message describing the error")},
)


base_user_model = Model(
    "User base model",
    {
        "id": fields.Integer(readonly=True, description="The user unique identifier"),
        "first_name": fields.String(required=True, description='The user first name'),
        "last_name": fields.String(required=True, description='The user last name'),
        "profile_picture": fields.String(
            required=False, description="URL pointing to the user's profile picture"
        ),
        "email": fields.String(required=True, description='The user email'),
    },
)


profile_model = base_user_model.clone(
    "User profile model",
    {"register_date": fields.DateTime(description='The date the user joined bookbnb')},
)
api.models[profile_model.name] = profile_model


register_model = base_user_model.clone(
    "User register model",
    {
        "password": fields.String(
            required=True, description='The password for the new user'
        ),
    },
)
api.models[register_model.name] = register_model


registered_model = profile_model.clone(
    "Registered user model",
    {
        "token": fields.String(
            required=True, attribute='password', description='The jwt'
        )
    },
)
api.models[registered_model.name] = registered_model


edit_model = api.model(
    "User edit model",
    {
        "first_name": fields.String(required=False, description='The user first name'),
        "last_name": fields.String(required=False, description='The user last name'),
        "profile_picture": fields.String(
            required=False, description="URL pointing to the user's profile picture"
        ),
        "email": fields.String(required=False, description='The user email'),
    },
)
