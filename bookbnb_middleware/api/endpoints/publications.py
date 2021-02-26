import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.publications_handlers import (
    block_publication,
    create_publication,
    get_publication,
    get_starrings,
    list_publications,
    replace_publication,
    star_publication,
    unstar_publication,
)
from bookbnb_middleware.api.models.publications_models import (
    error_model,
    filter_model,
    new_publication_model,
    new_star_model,
    publication_model,
    publication_star_parser,
    publication_star_uid_parser,
    base_publication_model,
    publication_image_model,
    loc_model,
    publication_question_model,
)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Publications",
    path="/bookbnb/publications",
    description="Operations related to bookbnb publications",
)

ns.models[base_publication_model.name] = base_publication_model
ns.models[error_model.name] = error_model
ns.models[new_publication_model.name] = new_publication_model
ns.models[new_star_model.name] = new_star_model
ns.models[publication_model.name] = publication_model
ns.models[publication_image_model.name] = publication_image_model
ns.models[loc_model.name] = loc_model
ns.models[publication_question_model.name] = publication_question_model


@ns.route("/")
class PublicationsResource(Resource):
    @ns.expect(new_publication_model)
    @ns.response(code=200, model=publication_model, description="Success")
    @ns.response(code=400, model=error_model, description="Bad request")
    def post(self):
        """
        Creates a new publication.
        """
        res, status_code = create_publication(request.json)
        return res, status_code

    @ns.response(code=200, model=publication_model, description="Success")
    @ns.response(code=400, model=error_model, description="Bad request")
    @ns.expect(filter_model)
    def get(self):
        """
        List all publications.
        """
        res, status_code = list_publications(filter_model.parse_args())
        return res, status_code


@ns.route("/<int:publication_id>")
@ns.param("publication_id", "The publication unique identifier")
class PublicationResource(Resource):
    @ns.response(code=200, model=publication_model, description="Success")
    @ns.response(code=404, model=error_model, description="Publication not found")
    def get(self, publication_id):
        """
        Get a publication by id.
        """
        res, status_code = get_publication(publication_id)
        return res, status_code

    @ns.response(200, model=publication_model, description="Success")
    @ns.response(400, model=error_model, description="Bad request")
    @ns.response(404, model=error_model, description="Publication not found")
    @ns.expect(new_publication_model)
    def put(self, publication_id):
        """
        Replace a publication by id.
        """
        res, status_code = replace_publication(publication_id, request.json)
        return res, status_code

    @ns.doc("block_publication")
    @ns.response(code=200, description="Publication successfully blocked")
    @ns.response(code=404, description="Publication not found")
    @ns.response(code=403, description="Publication has been already blocked")
    def delete(self, publication_id):
        """Block a publication."""
        res, status_code = block_publication(publication_id)
        return res, status_code


@ns.route("/<int:publication_id>/star")
@ns.param("publication_id", "The publication unique identifier")
class PublicationStarResource(Resource):
    @ns.doc("star_publication")
    @ns.response(code=200, model=new_star_model, description="Publication starred")
    @ns.response(
        code=403, model=error_model, description="Publication has been blocked"
    )
    @ns.response(code=404, model=error_model, description="Publication not found")
    @ns.expect(publication_star_uid_parser)
    def post(self, publication_id):
        """Star a publication."""
        params = publication_star_uid_parser.parse_args()
        res, status_code = star_publication(params, publication_id)
        return res, status_code

    @ns.doc("unstar_publication")
    @ns.response(200, "Publication unstarred")
    @ns.response(400, "Bad request")
    @ns.expect(publication_star_uid_parser)
    def delete(self, publication_id):
        """Unstar a publication."""
        params = publication_star_uid_parser.parse_args()
        res, status_code = unstar_publication(params, publication_id)
        return res, status_code

    @ns.doc("get_starrings")
    @ns.marshal_list_with(new_star_model)
    @ns.response(200, "Publications filtered")
    @ns.response(400, "Bad request")
    @ns.expect(publication_star_parser)
    def get(self, publication_id):
        """Get a starring."""
        params = publication_star_parser.parse_args()
        res, status_code = get_starrings(params, publication_id)
        return res, status_code
