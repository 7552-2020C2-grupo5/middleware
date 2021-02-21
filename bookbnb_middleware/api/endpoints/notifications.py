import logging
from flask import request
from flask_restx import Resource
from bookbnb_middleware.api.handlers.notifications_handlers import (
    create_instant_notification,
)
from bookbnb_middleware.api.models.notifications_models import (
    instant_notification_model,
)
from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace(
    name="Notifications",
    path="/bookbnb/notifications",
    description="Operations related to bookbnb notifications",
)


@ns.route('')
class InstantNotificationResource(Resource):
    @api.doc("create_instant_notification")
    @api.expect(instant_notification_model)
    @api.response(code=200, description="Successfully created")
    def post(self):
        """Create a new instant notification."""
        res, status_code = create_instant_notification(request.json)
        return res, status_code
