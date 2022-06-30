from django.urls import path

from apps.portal import views

urlpatterns = [
    # path(
    #     'register',
    #     views.RegisterPortalView.as_view(),
    #     name='register-portal'
    # ),
    path(
        '<portal_id>/add-staff',
        views.CreatePortalStaffView.as_view(),
        name='create-portal-staff'
    ),
]
