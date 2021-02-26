from flask_restx import fields, reqparse, Model

user_review_model = Model(
    "User review model",
    {
        "id": fields.Integer(description="The review identifier"),
        "reviewer_id": fields.Integer(
            description="The unique identifier of the reviewer"
        ),
        "reviewee_id": fields.Integer(
            description="The unique identifier of the reviewee"
        ),
        "booking_id": fields.Integer(
            description="The unique identifier of the booking the review belongs to"
        ),
        "score": fields.Integer(
            description="The score between 1 (lowest) and 4 (highest)."
        ),
        "comment": fields.String(description="User review optional comment"),
        "timestamp": fields.DateTime(
            description="The moment the review was created at"
        ),
    },
)

error_model = Model(
    "Reviews error model",
    {"message": fields.String(description="A message describing the error")},
)

reviewee_score_model = Model(
    "Reviewee score model",
    {
        "reviewee_id": fields.Integer(
            description="The unique identifier for the reviewee"
        ),
        "score_avg": fields.Float(description="The score average, possibly normalized"),
    },
)

new_user_review_model = Model(
    "New user's review model",
    {
        "reviewer_id": fields.Integer(
            required=True, description="The unique identifier of the reviewer"
        ),
        "reviewee_id": fields.Integer(
            required=True, description="The unique identifier of the reviewee"
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

user_review_parser = reqparse.RequestParser()
user_review_parser.add_argument(
    "booking_id",
    store_missing=False,
    type=int,
    help="The unique identifier for the booking",
)
user_review_parser.add_argument(
    "reviewer_id",
    store_missing=False,
    type=int,
    help="The unique identifier for the reviewer",
)
user_review_parser.add_argument(
    "reviewee_id",
    store_missing=False,
    type=int,
    help="The unique identifier of the reviewee",
)
