from rest_framework.exceptions import APIException


class ScheduleNotFound(APIException):
    default_detail = ('A schedule not found')


class BookingNotFound(APIException):
    default_detail = 'Booking not found.'
