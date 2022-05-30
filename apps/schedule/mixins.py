from apps.schedule.usecases import GetCounselingScheduleUseCase,GetBookingUseCase


class CounselingScheduleMixin:
    def get_counseling_schedule(self):
        return GetCounselingScheduleUseCase(counseling_schedule_id=self.kwargs.get('counseling_schedule_id')).execute()

class BookingMixin:
    def get_booking(self):
        return GetBookingUseCase(booking_id=self.kwargs.get('booking_id')).execute()
