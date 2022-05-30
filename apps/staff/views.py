from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAdminUser, AllowAny

from apps.core import generics
from apps.staff.mixins import StaffPositionMixin
from apps.staff import serializers
from apps.staff  import usecases


class AddStaffPositionView(generics.CreateAPIView):
    """
    Use this end-point to add Staff Positions
    """
    serializer_class = serializers.AddStaffPositionSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        return usecases.AddStaffPositionUseCase(serializer=serializer).execute()


class ListStaffPositionView(generics.ListAPIView):
    """
    Use this end-point to List  all Staff Positions
    """
    serializer_class = serializers.ListStaffPositionSerializer
    no_content_error_message = _('No staff positions at the moment')

    def get_queryset(self):
        return usecases.ListStaffPositionUseCase().execute()


class UpdateStaffPositionView(generics.UpdateAPIView, StaffPositionMixin):
    """
    Use this end-point to Update  Staff position.
    """

    serializer_class = serializers.UpdateStaffPositionSerializer
    queryset = ''
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.get_staff_position()

    def perform_update(self, serializer):
        return usecases.UpdateStaffPositionUseCase(
            serializer=serializer,
            staff_position=self.get_object()
        ).execute()


class DeleteStaffPositionView(generics.DestroyAPIView, StaffPositionMixin):
    """
    Use this end-point to Delete  Staff position view of specific Staff position
    """
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.get_staff_position()

    def perform_destroy(self, instance):
        return usecases.DeleteStaffPositionUseCase(
            staff_position=self.get_object()
        ).execute()
