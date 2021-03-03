from flask_restx import Model, fields, reqparse

error_model = Model(
    "Recommendations error model",
    {"message": fields.String(description="A message describing the error")},
)

recommendation_model = Model(
    "Recommendations",
    {
        "publication_id": fields.String(
            description="The id for the recommended publication."
        ),
        "score": fields.Float(description="The score assigned"),
    },
)

user_recommendations_model = Model(
    "User recommendations",
    {
        "recommendations": fields.List(
            fields.Nested(recommendation_model),
            description="Recommendations offered according to method.",
        ),
    },
)

max_fetch_parser = reqparse.RequestParser()
max_fetch_parser.add_argument(
    "max", type=int, help="Max recommendations to fetch", required=True
)

similarity_parser = reqparse.RequestParser()
similarity_parser.add_argument(
    "max", type=int, help="Max recommendations to fetch", required=True
)
similarity_parser.add_argument(
    "publication_id",
    type=int,
    help="The publication_id id to get recommendations for",
    required=True,
)

user_recommendation_parser = reqparse.RequestParser()
user_recommendation_parser.add_argument(
    "user_id", help="The user id to get recommendations for", type=int, required=True
)
user_recommendation_parser.add_argument(
    "max", type=int, help="Max recommendations to fetch", required=True
)
