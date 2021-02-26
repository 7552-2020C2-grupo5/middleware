import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.publication_reviews_handlers import (
    create_publication_review, get_publication_score,
    list_publications_reviews)
from bookbnb_middleware.api.models.publication_reviews_models import (
    error_model, new_publication_review_model, publication_review_model,
    publication_review_parser, publication_score_model)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Publications Reviews",
    path="/bookbnb/publication_reviews",
    description="Operations related to bookbnb publications reviews",
)


@ns.route("/reviews")
class PublicationReviewResource(Resource):
    @ns.doc("list_publication_review")
    @ns.marshal_list_with(publication_review_model)
    @ns.expect(publication_review_parser)
    def get(self):
        """List all publications reviews."""
        res, status_code = list_publications_reviews(
            publication_review_parser.parse_args()
        )
        return res, status_code

    @ns.doc("create_publication_review")
    @ns.expect(new_publication_review_model)
    @ns.response(
        code=200, model=publication_review_model, description="Successfully created"
    )
    @ns.response(code=400, model=error_model, description="Bad request")
    @ns.response(code=409, model=error_model, description="Already created")
    def post(self):
        """Create a new publication review."""
        res, status_code = create_publication_review(request.json)
        return res, status_code


@ns.route("/score/publication/<int:publication_id>")
class PublicationScoreResource(Resource):
    @ns.doc("get_publication_score")
    @ns.response(204, "No data for publication")
    @ns.response(200, "Score successfully calculated", model=publication_score_model)
    def get(self, publication_id):
        """Get score for publication."""
        res, status_code = get_publication_score(publication_id)
        return res, status_code
