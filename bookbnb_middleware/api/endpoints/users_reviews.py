import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.user_reviews_handlers import (
    create_user_review, get_reviewee_score, list_user_reviews)
from bookbnb_middleware.api.models.user_reviews_models import (
    error_model, new_user_review_model, reviewee_score_model,
    user_review_model, user_review_parser)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Users Reviews",
    path="/bookbnb/user_reviews",
    description="Operations related to bookbnb users reviews",
)


@ns.route("/reviews")
class UserReviewResource(Resource):
    @ns.doc("list_user_review")
    @ns.marshal_list_with(user_review_model)
    @ns.expect(user_review_parser)
    def get(self):
        """List all user reviews."""
        res, status_code = list_user_reviews(user_review_parser.parse_args())
        return res, status_code

    @ns.doc("create_user_review")
    @ns.expect(new_user_review_model)
    @ns.response(code=200, model=user_review_model, description="Successfully created")
    @ns.response(code=400, model=error_model, description="Bad request")
    @ns.response(code=409, model=error_model, description="Already created")
    def post(self):
        """Create a new user review."""
        res, status_code = create_user_review(request.json)
        return res, status_code


@ns.route("/score/user/<int:reviewee_id>")
class UserReviewRevieweeResource(Resource):
    @ns.doc("get_reviewee_score")
    @ns.response(204, "No data for user")
    @ns.response(200, "Score successfully calculated", model=reviewee_score_model)
    def get(self, reviewee_id):
        """Get score for reviewee."""
        res, status_code = get_reviewee_score(reviewee_id)
        return res, status_code
