from flask_restx import fields
from bookbnb_middleware.api.api import api

user_post = api.model('User post', {
    'name': fields.Integer(required=True, description='User name'),
    'last_name': fields.String(required=True, description='User last name'),
    'mail': fields.String(required=True, description='User mail'),
})
