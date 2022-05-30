from rest_framework.permissions import AllowAny

from apps.core import generics
from apps.portal import serializers, usecases
# from apps.portal.mixins import PortalMixin


# class RegisterPortalView(generics.CreateWithMessageAPIView):
#     """
#     Use this end-point to register portal
#     """
#     message = _('Registered successfully')
#     permission_classes = (AllowAny,)
#     serializer_class = serializers.RegisterPortalSerializer
#
#     def perform_create(self, serializer):
#         return usecases.RegisterPortalUseCase(
#             serializer=serializer
#         ).execute()
# from apps.portal.mixins import PortalMixin
#
#
# class CreatePortalStaffView(generics.CreateWithMessageAPIView, PortalMixin):
#     """
#     Use this end-point to create  portal staff
#     """
#     message = 'Portal staff created successfully'
#     serializer_class = serializers.CreatePortalStaffSerializer
#     permission_classes = (AllowAny,)
#
#     def get_object(self):
#         return self.get_portal()
#
#     def perform_create(self, serializer):
#         return usecases.CreatePortalStaffUseCase(
#             serializer=serializer,
#             portal=self.get_object()
#         ).execute()
