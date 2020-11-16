import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.bookbnb.users_handlers import (
    create_user,
)
from bookbnb_middleware.api.bookbnb.parsers import user_post_parser
from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace('bookbnb/users', description='Operations related to bookbnb users')


@ns.route('/')
class User(Resource):
    @api.expect(user_post_parser)
    @api.doc(responses={201: 'Success'})
    def post(self):
        """
        Creates a new user.
        """
        create_user(request.json)
        return 'Success', 201
