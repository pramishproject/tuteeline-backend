from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth.jwt import serializers, usecases
from apps.core import generics
from apps.core.mixins import LoggingErrorsMixin, ResponseMixin
from apps.user.mixins import ConsultancyUserMixin, PortalUserMixin,InstituteUserMixin


class StudentUserLoginView(generics.CreateWithMessageAPIView, ResponseMixin):
    """
    Use this end-point to get access token for normal user
    """
    throttle_scope = 'login'

    serializer_class = serializers.StudentUserLoginSerializer
    response_serializer_class = serializers.StudentUserLoginResponseSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        pass

    @swagger_auto_schema(responses={200: serializers.StudentUserLoginResponseSerializer()})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def response(self, result, serializer, status_code):
        response_serializer = self.get_response_serializer(serializer.validated_data)
        return Response(response_serializer.data, status=status_code)


class ConsultancyUserLoginView(generics.CreateAPIView, ResponseMixin):
    """
    Use this end-point to get login for consultancy user
    """
    # message = _('Please check your email for 6 digit OTP code.')
    serializer_class = serializers.ConsultancyUserLoginSerializer
    response_serializer_class = serializers.UserIdResponseSerializer

    def perform_create(self, serializer):
        return usecases.UserLoginWithOTPUseCase(self.request, serializer=serializer).execute()

    @swagger_auto_schema(responses={
        200: serializers.UserIdResponseSerializer()
    })
    def post(self, request, *args, **kwargs):

        return self.create(request, *args, **kwargs)

    def response(self, serializer, result, status_code):
        serializer = self.get_response_serializer(result)
        return Response(serializer.data)

class InstituteUserLoginView(ConsultancyUserLoginView):
    """
    use this endpoint to get login
    """
    serializer_class = serializers.InstituteUserLoginSerializer
    


class PortalUserLoginView(ConsultancyUserLoginView):
    """
    Use this end-point to get login for portal user
    """
    serializer_class = serializers.PortalUserLoginSerializer


class CustomTokenRefreshView(LoggingErrorsMixin, TokenRefreshView):
    logging_methods = ['POST']

    serializer_class = serializers.CustomTokenRefreshSerializer


class ConsultancyUser2FAVerifyView(generics.CreateAPIView, ConsultancyUserMixin, ResponseMixin):
    serializer_class = serializers.VerifyConsultanyUserOTPSerializer
    response_serializer_class = serializers.ConsultancyUserLoginResponseSerializer

    def get_object(self):
        return self.get_consultancy_user()

    def perform_create(self, serializer):
        pass

    @swagger_auto_schema(responses={
        200: serializers.ConsultancyUserLoginResponseSerializer()})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def response(self, result, serializer, status_code):
        response_serializer = self.get_response_serializer(serializer.validated_data)
        return Response(response_serializer.data)


class PortalUser2FAVerifyView(ConsultancyUser2FAVerifyView, PortalUserMixin):
    serializer_class = serializers.VerifyPortalUserOTPSerializer

    def get_object(self):
        return self.get_portal_user()

class InstituteUser2FAVerifyView(ConsultancyUser2FAVerifyView,InstituteUserMixin):
    """
    use this endpoint to verify otp
    """
    serializer_class=serializers.VerifyInstituteUserOTPSerializer
    def get_object(self):

        return self.get_institute_user()

class ResendOTPCodeView(generics.CreateWithMessageAPIView):
    """
    Use this end-point to resend OTP code for user
    """
    message = _('Please recheck your email for 6 digit OTP code.')
    serializer_class = serializers.ResendOTPCodeSerializer

    def perform_create(self, serializer):
        return usecases.ResendOTPCodeUseCase(serializer=serializer).execute()


class CreatePasswordForConsultancyStaffUserView(generics.CreateWithMessageAPIView, ConsultancyUserMixin):
    """
    Use this endpoint to save password of consultancy user
    """
    message = 'Password saved successfully.'
    serializer_class = serializers.CreatePasswordForConsultancyStaffSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.get_consultancy_user()

    def perform_create(self, serializer):
        return usecases.CreatePasswordForConsultancyUserUseCase(
            serializer=serializer,
            consultancy_user=self.get_object()
        ).execute()


class CreatePasswordForPortalStaffUserView(generics.CreateWithMessageAPIView, PortalUserMixin):
    """
    Use this endpoint to save password of portal user
    """
    message = 'Password saved successfully.'
    serializer_class = serializers.CreatePasswordForPortalStaffSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        print(self.get_portal_user())
        return self.get_portal_user()

    def perform_create(self, serializer):
        return usecases.CreatePasswordForPortalUserUseCase(
            serializer=serializer,
            portal_user=self.get_object()
        ).execute()


class ChangeConsultancyUserPasswordView(generics.CreateWithMessageAPIView, ConsultancyUserMixin):
    """
    Use this end point to change logged in consultancy user to change password
    """
    permission_classes = (AllowAny,)  # -> to be change
    message = _("Password changed successfully")
    serializer_class = serializers.ConsultancyUserChangePasswordSerializer

    def get_object(self):
        return self.get_consultancy_user()

    def perform_create(self, serializer):
        return usecases.ChangeConsultancyUserPasswordUseCase(
            serializer=serializer,
            consultancy_user=self.get_object()
        ).execute()
        
