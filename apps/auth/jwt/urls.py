from django.urls import path
from rest_framework_simplejwt.views import token_verify

from apps.auth.jwt import views
# from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path(
        'consultancy-user/login',
        views.ConsultancyUserLoginView.as_view(),
        name='consultancy-user-login'
    ),
    path(
        'portal-user/login',
        views.PortalUserLoginView.as_view(),
        name='portal-user-login'
    ),
    path(
        'student-user/login',
        views.StudentUserLoginView.as_view(),
        name='student-user-login'
    ),
    path(
        'institute-user/login',
        views.InstituteUserLoginView.as_view(),
        name='institute-user-login'

    ),
    path(
        'login-refresh',
        views.CustomTokenRefreshView.as_view(),
        name='login-refresh'
    ),
    path(
        'login-verify',
        token_verify,
        name='login-verify'
    ),
    path(
        'consultancy-user/<str:consultancy_user_id>/2fa/verify',
        views.ConsultancyUser2FAVerifyView.as_view(),
        name='consultancy-user-2fa-verify'
    ),
    path(
        'portal-user/<str:portal_user_id>/2fa/verify',
        views.PortalUser2FAVerifyView.as_view(),
        name='portal-user-2fa-verify'
    ),
    path(
        'institute-user/<str:institute_user_id>/2fa/verify',
        views.InstituteUser2FAVerifyView.as_view(),
        name='institute-user-2fa-verify'
    ),
    path(
        'user/resend-otp',
        views.ResendOTPCodeView.as_view(),
        name='consultancy-user-resend-otp'
    ),

    path(
        'consultancy-user/<str:consultancy_user_id>/change-password',
        views.ChangeConsultancyUserPasswordView.as_view(),
        name='consultancy-user-change-password'
    ),
    path(
        'consultancy-user/<str:consultancy_user_id>/create-password',
        views.CreatePasswordForConsultancyStaffUserView.as_view(),
        name='create-consultancy-user-staff-password'
    ),
    path(
        'portal-user/<str:portal_user_id>/create-password',
        views.CreatePasswordForPortalStaffUserView.as_view(),
        name='create-portal-user-staff-password'
    ),

]
# urlpatterns = format_suffix_patterns (urlpatterns)
