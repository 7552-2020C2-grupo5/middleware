import logging

from flask import request
from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.bookings_handlers import (
    accept_booking,
    create_intent_book,
    list_bookings,
    reject_booking,
)
from bookbnb_middleware.api.models.bookings_models import (
    accept_booking_model,
    booking_model,
    create_intent_book_model,
    error_model,
    filter_model,
    reject_booking_model,
)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Bookings",
    path="/bookbnb/bookings",
    description="Operations related to bookbnb bookings",
)

ns.models[accept_booking_model.name] = accept_booking_model
ns.models[booking_model.name] = booking_model
ns.models[create_intent_book_model.name] = create_intent_book_model
ns.models[error_model.name] = error_model
ns.models[reject_booking_model.name] = reject_booking_model


@ns.route("")
class BookingGetResource(Resource):
    @ns.marshal_list_with(booking_model)
    @ns.expect(filter_model)
    def get(self):
        """
        List all bookings.
        """
        res, status_code = list_bookings(filter_model.parse_args())
        return res, status_code


@ns.route("/intent_book")
class CreateIntentBookResource(Resource):
    @ns.expect(create_intent_book_model)
    @ns.response(code=200, model=booking_model, description="Success")
    @ns.response(code=412, model=error_model, description="Precondition Failed")
    @ns.response(code=400, model=error_model, description="Payment failed")
    def post(self):
        """
        Create new intent book.
        """
        res, status_code = create_intent_book(request.json)
        return res, status_code


@ns.route("/accept_booking")
class AcceptBookingResource(Resource):
    @ns.expect(accept_booking_model)
    @ns.response(code=200, description="Success")
    @ns.response(code=400, model=error_model, description="Payment failed")
    def post(self):
        """
        Accept a booking.
        """
        res, status_code = accept_booking(request.json)
        return res, status_code


@ns.route("/reject_booking")
class RejectBookingResource(Resource):
    @ns.expect(reject_booking_model)
    @ns.response(code=200, description="Success")
    @ns.response(code=400, model=error_model, description="Payment failed")
    def post(self):
        """
        Reject a booking.
        """
        res, status_code = reject_booking(request.json)
        return res, status_code
