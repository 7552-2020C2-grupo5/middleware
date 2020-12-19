from flask_restx import fields
from bookbnb_middleware.api.api import api


new_publication_question_model = api.model(
    "New publication question",
    {
        "question": fields.String(
            description="The question being asked", required=True
        ),
        "user_id": fields.Integer(
            description="The user asking the question", required=True
        ),
    },
)

publication_question_model = api.clone(
    "Publication question model",
    new_publication_question_model,
    {
        "id": fields.Integer(
            description="The unique identifier for the question", readonly=True
        ),
        "reply": fields.String(description="The reply to the question", required=False),
        "created_at": fields.DateTime(
            description="Timestamp the question was asked at"
        ),
        "replied_at": fields.DateTime(description="Timestamp the question was replied"),
    },
)

reply_model = api.model(
    "Publication reply model",
    {"reply": fields.String(description="The reply to the question", required=True)},
)
