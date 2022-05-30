from django.shortcuts import render

# Create your views here.
from apps.consultancy.mixins import ConsultancyStaffMixin
from apps.core import generics
from apps.schedule import usecases, serializers
from apps.schedule.filtersets import CounselorScheduleSearchFilter
from apps.schedule.mixins import CounselingScheduleMixin, BookingMixin
from apps.user.mixins import ConsultancyUserMixin


class AddCousellorScheduleView(generics.CreateAPIView, ConsultancyStaffMixin):
    """
    Use this endpoint to Add counselor schedule
    """
    serializer_class = serializers.AddCounsellingScheduleSerializer

    def get_object(self):
        return self.get_consultancy_staff()

    def perform_create(self, serializer):
        return usecases.AddCousellorScheduleUseCase(
            serializer=serializer,
            counsellor=self.get_object()

        ).execute()


class ListCounselorScheduleView(generics.ListAPIView, ConsultancyStaffMixin):
    """
    use this end point to list all counselor schedule
    """
    serializer_class = serializers.ListCounsellingScheduleSerializer
    filterset_class = CounselorScheduleSearchFilter

    def get_object(self):
        return self.get_consultancy_staff()

    def get_queryset(self):
        return usecases.ListCounselorScheduleUseCase(consultancy=self.get_consultancy_staff()).execute()


class AddBookingView(generics.CreateAPIView, CounselingScheduleMixin):
    """
    Use this end point to book counseling schedule
    """
    serializer_class = serializers.AddBookingSerializer

    def get_object(self):
        return self.get_counseling_schedule()

    def perform_create(self, serializer):
        return usecases.AddBookingUseCase(
            serializer=serializer,
            counseling_schedule=self.get_object()
        ).execute()


class ListBookingView(generics.ListAPIView):
    """
    Use this endpoint to list all bookings
    """
    serializer_class = serializers.ListBookingSerializer

    def get_queryset(self):
        return usecases.ListBookingUseCase().execute()


class UpdateCounselorScheduleView(generics.UpdateAPIView, CounselingScheduleMixin):
    """
    Use this endpoint to update counsellor schedules
    """
    serializer_class = serializers.UpdateCounsellingScheduleSerializer

    def get_object(self):
        return self.get_counseling_schedule()

    def perform_update(self, serializer):
        return usecases.UpdateCounselorScheduleUseCase(
            serializer=serializer,
            schedule=self.get_object()
        ).execute()


class DeleteCounsellorScheduleView(generics.DestroyAPIView,CounselingScheduleMixin):
    """
        Use this endpoint to delete counsellor schedules
    """

    def get_object(self):
        return self.get_counseling_schedule()

    def perform_destroy(self, instance):
        return usecases.DeleteCounsellorScheduleUseCase(
            schedule=self.get_object()
        ).execute()


class UpdateBookingView(generics.UpdateAPIView, BookingMixin):
    """
    Use this endpoint to update booking
    """
    serializer_class = serializers.UpdateBookingSerializer

    def get_object(self):
        return self.get_booking()

    def perform_update(self, serializer):
        return usecases.UpdateBookingUseCase(
            serializer=serializer,
            booking=self.get_object()
        ).execute()


class DeleteView(generics.DestroyAPIView,BookingMixin):
    """
        Use this endpoint to delete  booking
    """

    def get_object(self):
        return self.get_booking()

    def perform_destroy(self, instance):
        return usecases.DeleteBookingUseCase(
            booking=self.get_object()
        ).execute()

