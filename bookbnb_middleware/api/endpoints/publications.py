import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.publications_handlers import (
    create_publication,
    list_publications,
    get_publication,
)
from bookbnb_middleware.api.publications_models import (
    publication_post_parser,
    publication_get_parser,
    publication_get_serializer,
)

from bookbnb_middleware.api.api import api
from bookbnb_middleware.constants import SUCCESS_MSG

log = logging.getLogger(__name__)

ns = api.namespace(
    "bookbnb/publications", description="Operations related to bookbnb publications"
)


@ns.route("/")
class Publication(Resource):
    @api.expect(publication_post_parser, validate=True)
    @api.doc("create_publication", responses={201: SUCCESS_MSG})
    def post(self):
        """
        Creates a new publication.
        """
        create_publication(request.json)
        return None, 201

    @api.doc("list_publications", responses={200: SUCCESS_MSG})
    @api.expect(publication_get_parser, validate=True)
    @api.marshal_list_with(publication_get_serializer)
    def get(self):
        """
        List all publications.
        """
        res = list_publications(publication_get_parser.parse_args())
        return res, 200


@ns.route("/<int:publication_id>")
@api.param("publication_id", "The publication unique identifier")
@api.response(200, SUCCESS_MSG)
class PublicationById(Resource):
    @api.doc("get_publication_by_id")
    @api.marshal_with(publication_get_serializer)
    def get(self, publication_id):
        """
        Get a publication by id.
        """
        res = get_publication(publication_id)
        return res, 200
