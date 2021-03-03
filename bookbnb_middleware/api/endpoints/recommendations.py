import logging

from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.recommendations_handlers import (
    get_latest_publications,
    get_popular_publications,
    get_similar_publications,
    get_reviews_cf,
    get_stars_cf,
)
from bookbnb_middleware.api.models.recommendations_models import (
    error_model,
    max_fetch_parser,
    similarity_parser,
    user_recommendation_parser,
    recommendation_model,
    user_recommendations_model,
)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Recommendations",
    path="/bookbnb/recommendations",
    description="Operations related to bookbnb recommendations",
)

ns.models[error_model.name] = error_model
ns.models[recommendation_model.name] = recommendation_model
ns.models[user_recommendations_model.name] = user_recommendations_model


@ns.route("/latest")
class LatestRecommendationResource(Resource):
    @ns.expect(max_fetch_parser)
    @ns.response(code=200, model=user_recommendations_model, description="Success")
    @ns.response(code=204, description="No recommendations available")
    def post(self):
        """
        Get latest publications recommended
        """
        res, status_code = get_latest_publications(max_fetch_parser.parse_args())
        return res, status_code


@ns.route("/popular")
class PopularRecommendationResource(Resource):
    @ns.expect(max_fetch_parser)
    @ns.response(code=200, model=user_recommendations_model, description="Success")
    @ns.response(code=204, description="No recommendations available")
    def post(self):
        """
        Get most popular publications recommended
        """
        res, status_code = get_popular_publications(max_fetch_parser.parse_args())
        return res, status_code


@ns.route("/publications")
class SimilarRecommendationResource(Resource):
    @ns.expect(similarity_parser)
    @ns.response(code=200, model=user_recommendations_model, description="Success")
    @ns.response(code=204, description="No recommendations available")
    def post(self):
        """
        Get recommendations based on publications similarity
        """
        res, status_code = get_similar_publications(similarity_parser.parse_args())
        return res, status_code


@ns.route("/reviews")
class ReviewsBasedRecommendationResource(Resource):
    @ns.expect(user_recommendation_parser)
    @ns.response(code=200, model=user_recommendations_model, description="Success")
    @ns.response(code=204, description="No recommendations available")
    def post(self):
        """
        Get CF recommendations based on reviews scores
        """
        res, status_code = get_reviews_cf(user_recommendation_parser.parse_args())
        return res, status_code


@ns.route("/stars")
class StarsBasedRecommendationResource(Resource):
    @ns.expect(user_recommendation_parser)
    @ns.response(code=200, model=user_recommendations_model, description="Success")
    @ns.response(code=204, description="No recommendations available")
    def post(self):
        """
        Get CF recommendations based on starred publications
        """
        res, status_code = get_stars_cf(user_recommendation_parser.parse_args())
        return res, status_code
