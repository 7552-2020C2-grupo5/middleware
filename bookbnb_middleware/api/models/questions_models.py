from flask_restx import Model, fields

new_publication_question_model = Model(
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

publication_question_model = new_publication_question_model.clone(
    "Publication question model",
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

reply_model = Model(
    "Publication reply model",
    {"reply": fields.String(description="The reply to the question", required=True)},
)

error_model = Model(
    "Publications error model",
    {"message": fields.String(description="A message describing the error")},
)
