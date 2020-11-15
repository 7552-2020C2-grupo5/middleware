import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.bookbnb.users_handlers import (
    create_user,
)
from bookbnb_middleware.api.bookbnb.serializers import user_post
from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace('bookbnb/users', description='Operations related to bookbnb users')


@ns.route('/')
class User(Resource):
    @api.expect(user_post)
    def post(self):
        """
        Creates a new user.
        """
        create_user(request.json)
        return None, 201
