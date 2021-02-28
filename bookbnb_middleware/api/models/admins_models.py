from flask_restx import Model, fields, reqparse

login_model = Model(
    "Admin login model",
    {
        "email": fields.String(required=True, description="Account email"),
        "password": fields.String(required=True, description="Account password"),
    },
)

logged_model = Model(
    "Admin logged model",
    {"token": fields.String(description="The admin session token")},
)

auth_model = reqparse.RequestParser()
auth_model.add_argument(
    "Authorization", type=str, location="headers", help="Access token", required=True
)

admin_parser = reqparse.RequestParser()
admin_parser.add_argument(
    "first_name",
    type=str,
    help="First name to filter on",
    store_missing=False,
)
admin_parser.add_argument(
    "last_name",
    type=str,
    help="Last name to filter on",
    store_missing=False,
)
admin_parser.add_argument(
    "email",
    type=str,
    help="Email to filter on",
    store_missing=False,
)

logged_out_model = Model(
    "Admin logged out model",
    {
        "message": fields.String(description="A message describing the session status"),
        "status": fields.String(description="Session status"),
    },
)

error_model = Model(
    "Admin error model",
    {"message": fields.String(description="A message describing the error")},
)

success_model = Model(
    "Admin success model",
    {"status": fields.String(description="A description of the status")},
)

email_model = Model(
    "Admin email model", {"email": fields.String(description="Admin email")}
)

base_admin_model = Model(
    "Admin base model",
    {
        "id": fields.Integer(readonly=True, description="The admin unique identifier"),
        "first_name": fields.String(required=True, description="The admin first name"),
        "last_name": fields.String(required=True, description="The admin last name"),
        "email": fields.String(required=True, description="The admin email"),
    },
)

profile_model = base_admin_model.clone(
    "Admin profile model",
    {"register_date": fields.DateTime(description="The date the admin was registered")},
)

register_model = base_admin_model.clone(
    "Admin register model",
    {
        "password": fields.String(
            required=True, description="The password for the new admin"
        ),
    },
)

registered_model = profile_model.clone(
    "Registered admin model",
    {
        "token": fields.String(
            required=True, attribute="password", description="The jwt"
        )
    },
)

edit_model = Model(
    "Admin edit model",
    {
        "first_name": fields.String(required=False, description="The admin first name"),
        "last_name": fields.String(required=False, description="The admin last name"),
    },
)
