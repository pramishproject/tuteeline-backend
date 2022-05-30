from django.db import IntegrityError
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.consultancy.models import ConsultancyStaff
from apps.core.usecases import BaseUseCase
from apps.schedule.exceptions import ScheduleNotFound, BookingNotFound
from apps.schedule.models import CounsellingSchedule, Booking
from django.core.exceptions import ValidationError as DjangoValidationError


class AddCousellorScheduleUseCase(BaseUseCase):
    def __init__(self, serializer, counsellor: ConsultancyStaff):
        self._serializer = serializer
        self._counsellor = counsellor
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._schedule = CounsellingSchedule(
            **self._data,
            counsellor=self._counsellor
        )
        try:
            self._schedule.clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)
        self._schedule.save()


class ListCounselorScheduleUseCase(BaseUseCase):
    def __init__(self, consultancy: ConsultancyStaff):
        self._consultancy = consultancy

    def execute(self):
        self._factory()
        return self._schedule

    def _factory(self):
        self._schedule = CounsellingSchedule.objects.filter(is_archived=False)


class GetCounselingScheduleUseCase(BaseUseCase):
    def __init__(self, counseling_schedule_id: CounsellingSchedule):
        self._counseling_schedule_id = counseling_schedule_id

    def execute(self):
        self._factory()
        return self._counseling_schedule

    def _factory(self):
        try:
            self._counseling_schedule = CounsellingSchedule.objects.get(pk=self._counseling_schedule_id)
        except CounsellingSchedule.DoesNotExist:
            raise ScheduleNotFound


class AddBookingUseCase(BaseUseCase):
    def __init__(self, serializer, counseling_schedule):
        self._counseling_schedule = counseling_schedule
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        try:
            if self._counseling_schedule.status == 'AVAILABLE':
                self._booking = Booking(**self._data, schedule=self._counseling_schedule)
                self._booking.is_booked = True
                self._counseling_schedule.status = 'BUSY'
                self._counseling_schedule.save()
                self._booking.save()
        except IntegrityError:
            raise ValidationError({'schedule': 'Booking already exists for following schedule.'})


class ListBookingUseCase(BaseUseCase):
    def execute(self):
        self._factory()
        return self._booking

    def _factory(self):
        self._booking = Booking.objects.all()


class UpdateCounselorScheduleUseCase(BaseUseCase):
    def __init__(self, serializer, schedule: CounsellingSchedule):
        self._schedule = schedule
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._schedule, data, self._data[data])
        self._schedule.updated_at = timezone.now()
        try:
            self._schedule.clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)
        self._schedule.save()


class DeleteCounsellorScheduleUseCase(BaseUseCase):
    def __init__(self, schedule: CounsellingSchedule):
        self._schedule = schedule

    def execute(self):
        self._factory()

    def _factory(self):
        self._schedule.delete()


class GetBookingUseCase(BaseUseCase):
    def __init__(self, booking_id: Booking):
        self._booking_id = booking_id

    def execute(self):
        self._factory()
        return self._booking

    def _factory(self):
        try:
            self._booking = Booking.objects.get(pk=self._booking_id)
        except Booking.DoesNotExist:
            raise BookingNotFound


class UpdateBookingUseCase(BaseUseCase):
    def __init__(self, serializer, booking: Booking):
        self._booking = booking
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
                setattr(self._booking, data, self._data[data])
        self._booking.updated_at = timezone.now()
        self._booking.save()


class DeleteBookingUseCase(BaseUseCase):
    def __init__(self, booking: Booking):
        self._booking = booking

    def execute(self):
        self._factory()

    def _factory(self):
        self._booking.delete()
