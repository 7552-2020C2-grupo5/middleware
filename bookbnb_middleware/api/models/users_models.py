from flask_restx import Model, fields, reqparse

login_model = Model(
    "User login model",
    {
        "email": fields.String(required=True, description="Account email"),
        "password": fields.String(required=True, description="Account password"),
        "push_token": fields.String(required=True, description="Push token"),
    },
)

logged_model = Model(
    "User logged model", {"token": fields.String(description="The user session token")}
)

auth_model = reqparse.RequestParser()
auth_model.add_argument(
    "Authorization", type=str, location="headers", help="Access token", required=True
)

user_parser = reqparse.RequestParser()
user_parser.add_argument(
    "first_name",
    type=str,
    help="First name to filter on",
    store_missing=False,
)
user_parser.add_argument(
    "last_name",
    type=str,
    help="Last name to filter on",
    store_missing=False,
)
user_parser.add_argument(
    "email",
    type=str,
    help="Email to filter on",
    store_missing=False,
)

logged_out_model = Model(
    "User logged out model",
    {
        "message": fields.String(description="A message describing the session status"),
        "status": fields.String(description="Session status"),
    },
)

error_model = Model(
    "User error model",
    {"message": fields.String(description="A message describing the error")},
)

success_model = Model(
    "User success model",
    {"status": fields.String(description="A description of the status")},
)

email_model = Model(
    "User email model", {"email": fields.String(description="User email")}
)

base_user_model = Model(
    "User base model",
    {
        "id": fields.Integer(readonly=True, description="The user unique identifier"),
        "first_name": fields.String(required=True, description="The user first name"),
        "last_name": fields.String(required=True, description="The user last name"),
        "profile_picture": fields.String(
            required=False, description="URL pointing to the user's profile picture"
        ),
        "email": fields.String(required=True, description="The user email"),
    },
)

profile_model = base_user_model.clone(
    "User profile model",
    {"register_date": fields.DateTime(description="The date the user joined bookbnb")},
)

register_model = base_user_model.clone(
    "User register model",
    {
        "password": fields.String(
            required=True, description="The password for the new user"
        ),
    },
)

registered_model = profile_model.clone(
    "Registered user model",
    {
        "token": fields.String(
            required=True, attribute="password", description="The jwt"
        )
    },
)

edit_model = Model(
    "User edit model",
    {
        "first_name": fields.String(required=False, description="The user first name"),
        "last_name": fields.String(required=False, description="The user last name"),
        "profile_picture": fields.String(
            required=False, description="URL pointing to the user's profile picture"
        ),
        "email": fields.String(required=False, description="The user email"),
    },
)
