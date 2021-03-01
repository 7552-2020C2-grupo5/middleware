from flask_restx import Model, fields, reqparse

oauth_token_parser = reqparse.RequestParser()
oauth_token_parser.add_argument(
    'token', type=str, required=True, help="The OAuth token"
)

error_model = Model(
    "OAuth error model",
    {"message": fields.String(description="A message describing the error")},
)

login_model = Model(
    "OAuth login model",
    {
        "push_token": fields.String(required=True, description="Push token"),
    },
)
