import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.handlers.publications_handlers import (
    create_publication,
    list_publications,
    get_publication,
    replace_publication,
    block_publication,
)
from bookbnb_middleware.api.models.publications_models import (
    publication_model,
    filter_model,
    new_publication_model,
    error_model,
)

from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace(
    name="Publications",
    path="/bookbnb/publications",
    description="Operations related to bookbnb publications",
)


@ns.route("/")
class PublicationsResource(Resource):
    @api.expect(new_publication_model)
    @api.response(code=200, model=publication_model, description="Success")
    @api.response(code=400, model=error_model, description="Bad request")
    def post(self):
        """
        Creates a new publication.
        """
        res, status_code = create_publication(request.json)
        return res, status_code

    @api.response(code=200, model=publication_model, description="Success")
    @api.response(code=400, model=error_model, description="Bad request")
    @api.expect(filter_model)
    def get(self):
        """
        List all publications.
        """
        res, status_code = list_publications(filter_model.parse_args())
        return res, status_code


@ns.route("/<int:publication_id>")
@api.param("publication_id", "The publication unique identifier")
class PublicationResource(Resource):
    @api.response(code=200, model=publication_model, description="Success")
    @api.response(code=404, model=error_model, description="Publication not found")
    def get(self, publication_id):
        """
        Get a publication by id.
        """
        res, status_code = get_publication(publication_id)
        return res, status_code

    @api.response(200, model=publication_model, description="Success")
    @api.response(404, model=error_model, description='Publication not found')
    @api.expect(new_publication_model)
    def put(self, publication_id):
        """
        Replace a publication by id.
        """
        res, status_code = replace_publication(publication_id, request.json)
        return res, status_code

    @api.doc("block_publication")
    @api.response(code=200, description="Publication successfully blocked")
    @api.response(code=404, description="Publication not found")
    @api.response(code=403, description="Publication has been already blocked")
    def delete(self, publication_id):
        """Block a publication."""
        res, status_code = block_publication(publication_id)
        return res, status_code
