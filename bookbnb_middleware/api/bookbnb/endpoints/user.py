import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.bookbnb.user_handlers import create_user, list_users
from bookbnb_middleware.api.bookbnb.parsers import user_post_parser
from bookbnb_middleware.api.bookbnb.serializers import user_get_serializer
from bookbnb_middleware.api.api import api
from bookbnb_middleware.constants import SUCCESS_MSG

log = logging.getLogger(__name__)

ns = api.namespace('bookbnb/user', description='Operations related to bookbnb users')


@ns.route('/')
class User(Resource):
    @api.expect(user_post_parser)
    @api.doc('create_user', responses={201: SUCCESS_MSG})
    def post(self):
        """
        Creates a new user.
        """
        create_user(request.json)
        return None, 201

    @api.doc('list_users')
    @api.marshal_list_with(user_get_serializer)
    def get(self):
        """
        List all users.
        """
        res = list_users()
        return res, 200
