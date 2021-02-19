import logging
from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.handlers.user_reviews_handlers import (
    list_user_reviews,
    create_user_review,
    get_reviewee_score,
)
from bookbnb_middleware.api.models.user_reviews_models import (
    user_review_model,
    new_user_review_model,
    user_review_parser,
    error_model,
    reviewee_score_model,
)
from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace(
    name="Users Reviews",
    path="/bookbnb/user_reviews",
    description="Operations related to bookbnb users reviews",
)


@ns.route('/reviews')
class UserReviewResource(Resource):
    @api.doc("list_user_review")
    @api.marshal_list_with(user_review_model)
    @api.expect(user_review_parser)
    def get(self):
        """List all user reviews."""
        res, status_code = list_user_reviews(user_review_parser.parse_args())
        return res, status_code

    @api.doc("create_user_review")
    @api.expect(new_user_review_model)
    @api.response(code=200, model=user_review_model, description="Successfully created")
    @api.response(code=400, model=error_model, description="Bad request")
    @api.response(code=409, model=error_model, description="Already created")
    def post(self):
        """Create a new user review."""
        res, status_code = create_user_review(request.json)
        return res, status_code


@ns.route("/score/user/<int:reviewee_id>")
class UserReviewRevieweeResource(Resource):
    @api.doc("get_reviewee_score")
    @api.response(204, "No data for user")
    @api.response(200, "Score successfully calculated", model=reviewee_score_model)
    def get(self, reviewee_id):
        """Get score for reviewee."""
        res, status_code = get_reviewee_score(reviewee_id)
        return res, status_code
