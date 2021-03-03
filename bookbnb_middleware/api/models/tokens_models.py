from flask_restx import Model, fields

server_token_model = Model("Server token", {"token": fields.String(required=True)})

error_model = Model(
    "Tokens error model",
    {"message": fields.String(description="A message describing the error")},
)
