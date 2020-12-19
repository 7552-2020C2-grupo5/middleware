import logging

from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.handlers.questions_handlers import (
    create_question,
    reply_question,
)
from bookbnb_middleware.api.models.questions_models import (
    new_publication_question_model,
    publication_question_model,
    error_model,
    reply_model,
)
from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace(
    name="Questions",
    path="/bookbnb/publications",
    description="Operations related to bookbnb publications questions",
)


@ns.route("/<int:publication_id>/questions")
@ns.param("publication_id", "The publication unique identifier")
class PublicationQuestionListResource(Resource):
    @api.expect(new_publication_question_model)
    @api.response(code=200, model=publication_question_model, description="Success")
    @api.response(code=404, model=error_model, description="Publication not found")
    def post(self, publication_id):
        res, status_code = create_question(publication_id, request.json)
        return res, status_code


@ns.route("/<int:publication_id>/questions/<int:question_id>")
@api.param("publication_id", "The publication unique identifier")
@api.param("question_id", "The question unique identifier")
class PublicationResource(Resource):
    @api.expect(reply_model)
    @api.response(
        code=200, model=publication_question_model, description="Question updated"
    )
    @api.response(
        code=404, model=error_model, description="Publication or question not found"
    )
    def patch(self, publication_id, question_id):
        res, status_code = reply_question(publication_id, question_id, request.json)
        return res, status_code
