import logging
from flask_restx import Resource

from bookbnb_middleware.api.handlers.bookings_handlers import list_bookings
from bookbnb_middleware.api.models.bookings_models import (
    new_booking_model,
    booking_model,
    filter_model,
    error_model,
)

from bookbnb_middleware.api.api import api

log = logging.getLogger(__name__)

ns = api.namespace(
    name="Bookings",
    path="/bookbnb/bookings",
    description="Operations related to bookbnb bookings",
)


@ns.route('')
class BookingGetResource(Resource):
    @api.marshal_list_with(booking_model)
    @api.expect(filter_model)
    def get(self):
        """
        List all bookings.
        """
        res, status_code = list_bookings(filter_model.parse_args())
        return res, status_code

    @api.expect(new_booking_model)
    @ns.response(code=201, model=booking_model, description='Success')
    @ns.response(code=412, model=error_model, description='Precondition Failed')
    def post(self):
        """
        Create new booking.
        """
        return None, 201  # todo
