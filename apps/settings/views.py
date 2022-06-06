from django.shortcuts import render
from rest_framework.permissions import AllowAny

from apps.core import generics

# Create your views here.
from django.utils.translation import gettext_lazy as _
from apps.settings import serializers, usecases
from apps.settings.mixins import SettingMixin


class AddColorView(generics.CreateWithMessageAPIView):
    """
    Use this endpoint to add color.
    """
    message = _("Color saved successfully")
    serializer_class = serializers.AddSettingColorSerializer

    def perform_create(self, serializer):
        return usecases.AddColorUseCase(serializer=serializer).execute()


class ListSettingColorView(generics.ListAPIView):
    """
    Use this endpoint to list all color.
    """
    serializer_class = serializers.ListSettingColorSerializer
    no_content_error_message = _("No data at the moment")

    def get_queryset(self):
        return usecases.ListSettingColorUseCase().execute()


class UpdateSettingColorView(generics.UpdateWithMessageAPIView, SettingMixin):
    """
    Use this end-point to Update  Setting color.
    """
    message = _('Color updated successfully')

    serializer_class = serializers.UpdateColorSerializer
    queryset = ''
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.get_setting()

    def perform_update(self, serializer):
        return usecases.UpdateSettingColorUseCase(
            serializer=serializer,
            setting=self.get_object()
        ).execute()

class Update2FAView(generics.UpdateWithMessageAPIView,SettingMixin):
    message = _("2fa update successfully")
    serializer_class = serializers.Update2FASerializer
    queryset = ''
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.get_setting()

    def perform_update(self, serializer):
        return usecases.UpdateSettingColorUseCase(
            serializer=serializer,
            setting=self.get_object()
        ).execute()