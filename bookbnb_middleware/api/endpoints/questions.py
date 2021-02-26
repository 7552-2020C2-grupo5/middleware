import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.questions_handlers import (
    create_question, reply_question)
from bookbnb_middleware.api.models.questions_models import (
    error_model, new_publication_question_model, publication_question_model,
    reply_model)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Questions",
    path="/bookbnb/publications",
    description="Operations related to bookbnb publications questions",
)


@ns.route("/<int:publication_id>/questions")
@ns.param("publication_id", "The publication unique identifier")
class PublicationQuestionListResource(Resource):
    @ns.expect(new_publication_question_model)
    @ns.response(code=200, model=publication_question_model, description="Success")
    @ns.response(code=404, model=error_model, description="Publication not found")
    def post(self, publication_id):
        res, status_code = create_question(publication_id, request.json)
        return res, status_code


@ns.route("/<int:publication_id>/questions/<int:question_id>")
@ns.param("publication_id", "The publication unique identifier")
@ns.param("question_id", "The question unique identifier")
class PublicationResource(Resource):
    @ns.expect(reply_model)
    @ns.response(
        code=200, model=publication_question_model, description="Question updated"
    )
    @ns.response(
        code=404, model=error_model, description="Publication or question not found"
    )
    def patch(self, publication_id, question_id):
        res, status_code = reply_question(publication_id, question_id, request.json)
        return res, status_code
