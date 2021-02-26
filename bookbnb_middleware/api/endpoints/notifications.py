import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.notifications_handlers import (
    create_instant_notification,
)
from bookbnb_middleware.api.models.notifications_models import (
    instant_notification_model,
)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Notifications",
    path="/bookbnb/notifications",
    description="Operations related to bookbnb notifications",
)

ns.models[instant_notification_model.name] = instant_notification_model


@ns.route("")
class InstantNotificationResource(Resource):
    @ns.doc("create_instant_notification")
    @ns.expect(instant_notification_model)
    @ns.response(code=200, description="Successfully created")
    def post(self):
        """Create a new instant notification."""
        res, status_code = create_instant_notification(request.json)
        return res, status_code
