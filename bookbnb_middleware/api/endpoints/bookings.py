import logging
from flask_restx import Resource
from flask import request

from bookbnb_middleware.api.handlers.bookings_handlers import (
    list_bookings,
    create_intent_book,
    accept_booking,
    reject_booking,
)
from bookbnb_middleware.api.models.bookings_models import (
    create_intent_book_model,
    accept_booking_model,
    reject_booking_model,
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


@ns.route('/intent_book')
class CreateIntentBookResource(Resource):
    @api.expect(create_intent_book_model)
    @ns.response(code=200, model=booking_model, description='Success')
    @ns.response(code=412, model=error_model, description='Precondition Failed')
    @ns.response(code=400, model=error_model, description='Payment failed')
    def post(self):
        """
        Create new intent book.
        """
        res, status_code = create_intent_book(request.json)
        return res, status_code


@ns.route('/accept_booking')
class AcceptBookingResource(Resource):
    @api.expect(accept_booking_model)
    @ns.response(code=200, description='Success')
    @ns.response(code=400, model=error_model, description='Payment failed')
    def post(self):
        """
        Accept a booking.
        """
        res, status_code = accept_booking(request.json)
        return res, status_code


@ns.route('/reject_booking')
class RejectBookingResource(Resource):
    @api.expect(reject_booking_model)
    @ns.response(code=200, description='Success')
    @ns.response(code=400, model=error_model, description='Payment failed')
    def post(self):
        """
        Reject a booking.
        """
        res, status_code = reject_booking(request.json)
        return res, status_code
