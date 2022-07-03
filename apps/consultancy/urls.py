from django.urls import path

from apps.consultancy import views

urlpatterns = [
    path(
        'register',
        views.RegisterConsultancyView.as_view(),
        name='register-consultancy'
    ),
    path(
        '<consultancy_id>/add-staff',
        views.CreateConsultancyStaffView.as_view(),
        name='create-consultancy-staff'
    ),
    path(
        '<consultancy_id>/list',
        views.ListConsultancyStaffView.as_view(),
        name='list-consultancy-staff'
    ),
    # path(
    #     'consultancy_staff/<consultancy_staff_id>/update',
    #     views.UpdateConsultancyStaffView.as_view(),
    #     name='update-consultancy-staff'
    # ),
    path(
        'consultancy-staff/<consultancy_staff_id>/update',
        views.UpdateConsultancyStaffView.as_view(),
        name='update-consultancy-staff'
    ),
    path(
        'consultancy-staff/<consultancy_staff_id>/update-photo',
        views.UpdateConsultancyStaffPhotoView.as_view(),
        name='update-consultancy-staff-photo'
    ),
    path(
        'list',
        views.ListConsultancyView.as_view(),
        name='list-consultancy'
    ),
    path(
        'consultancy-user/<str:consultancy_user_id>/deactivate',
        views.DeactivateConsultancyUserView.as_view(),
        name='deactivate-consultancy-user'
    ),
    path(
        'consultancy-user/<str:consultancy_user_id>/activate',
        views.ActivateConsultancyUserView.as_view(),
        name='activate-consultancy-user'
    ),
    path(
        '<consultancy_id>/consultancy/detail',
        views.ConsultancyDetail.as_view(),
        name = ""
    ),
    path(
        '<consultancy_id>/broucher/update',
        views.UpdateConsultancyBrochure.as_view(),
        name="broucher-update"
    ),


]
