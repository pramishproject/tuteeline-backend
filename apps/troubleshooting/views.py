from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from apps.consultancy.mixins import ConsultancyStaffMixin
from apps.core import generics

# Create your views here.
from apps.troubleshooting import serializers, usecases
from apps.troubleshooting.mixins import TroubleshootMixin
from apps.user.mixins import ConsultancyUserMixin


class AddTroubleShootTicketView(generics.CreateWithMessageAPIView, ConsultancyStaffMixin):
    """
    Use this endpoint to add trouble shoot
    """
    message = _("Ticket added successfully")
    serializer_class = serializers.AddTroubleshootTicketSerializer

    def get_object(self):
        return self.get_consultancy_staff()

    def perform_create(self, serializer):
        return usecases.AddTroubleShootTicketUseCase(
            serializer=serializer,
            consultancy_user=self.get_object()
        ).execute()


class ListTroubleShootTicketView(generics.ListAPIView):
    """
    Use this endpoint to  list  trouble shoots
    """
    serializer_class = serializers.ListTroubleShootTicketSerializer

    def get_queryset(self):
        return usecases.ListTroubleShootTicketUseCases().execute()


class UpdateTroubleShootStatusView(generics.CreateWithMessageAPIView, TroubleshootMixin):
    """
    Use this endpoint to update or assign trouble shoot
    """
    message = _("Ticket update successfully")
    serializer_class = serializers.UpdateTravelshootSerializer

    def get_object(self):
        return self.get_troubleshoot()

    def perform_create(self, serializer):
        return usecases.UpdateTroubleShootUseCase(serializer=serializer,troubleshoot=self.get_object()).execute()


