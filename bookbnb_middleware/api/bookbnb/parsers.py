from flask_restx import fields
from bookbnb_middleware.api.api import api

user_post_parser = api.model(
    'User post',
    {
        'first_name': fields.String(required=True, description='User name'),
        'last_name': fields.String(required=True, description='User last name'),
        'email': fields.String(required=True, description='User mail'),
    },
)
