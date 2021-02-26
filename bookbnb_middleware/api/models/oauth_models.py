from flask_restx import Model, fields, reqparse

oauth_token_parser = reqparse.RequestParser()
oauth_token_parser.add_argument(
    'token', type=str, required=True, help="The OAuth token"
)

oauth_parser = reqparse.RequestParser()
oauth_parser.add_argument(
    "Authorization", type=str, location="headers", help="Access token", required=True
)

error_model = Model(
    "OAuth error model",
    {"message": fields.String(description="A message describing the error")},
)
