from flask_restx import fields, reqparse, Model

publication_review_model = Model(
    "Publication review model",
    {
        "id": fields.Integer(description="The review identifier"),
        "reviewer_id": fields.Integer(
            description="The unique identifier of the reviewer"
        ),
        "publication_id": fields.Integer(
            description="The unique identifier of the reviewed publication"
        ),
        "booking_id": fields.Integer(
            description="The unique identifier of the booking the review belongs to"
        ),
        "score": fields.Integer(
            description="The score between 1 (lowest) and 4 (highest)."
        ),
        "comment": fields.String(description="An optional comment"),
        "timestamp": fields.DateTime(
            description="The moment the review was created at"
        ),
    },
)

error_model = Model(
    "Reviews error model",
    {"message": fields.String(description="A message describing the error")},
)

publication_score_model = Model(
    "Publication score model",
    {
        "publication_id": fields.Integer(
            description="The unique identifier for the reviewed publication"
        ),
        "score_avg": fields.Float(description="The score average, possibly normalized"),
    },
)

new_publication_review_model = Model(
    "New publication's review model",
    {
        "reviewer_id": fields.Integer(
            required=True, description="The unique identifier of the reviewer"
        ),
        "publication_id": fields.Integer(
            description="The unique identifier of the reviewed publication"
        ),
        "booking_id": fields.Integer(
            required=True,
            description="The unique identifier of the booking the review belongs to",
        ),
        "score": fields.Integer(
            required=True, description="The score between 1 (lowest) and 4 (highest)."
        ),
        "comment": fields.String(required=False, description="An optional comment"),
    },
)

publication_review_parser = reqparse.RequestParser()
publication_review_parser.add_argument(
    "booking_id",
    store_missing=False,
    type=int,
    help="The unique identifier for the booking",
)
publication_review_parser.add_argument(
    "reviewer_id",
    store_missing=False,
    type=int,
    help="The unique identifier for the reviewer",
)
publication_review_parser.add_argument(
    "publication_id",
    store_missing=False,
    type=int,
    help="The unique identifier of the publication",
)
