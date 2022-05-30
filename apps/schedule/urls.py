from django.urls import path

from apps.schedule import views

urlpatterns = [
    path(
        'consultancy-staff/<consultancy_staff_id>/add',
        views.AddCousellorScheduleView.as_view(),
        name = 'add-counsellor-schedule'
    ),
    path(
        'consultancy-staff/<consultancy_staff_id>/list',
        views.ListCounselorScheduleView.as_view(),
        name='list-counsellor-schedule'

    ),
    path(
        '<counseling_schedule_id>/booking/add',
        views.AddBookingView.as_view(),
        name='add-booking'

    ),
    path(
        '<counseling_schedule_id>/update',
        views.UpdateCounselorScheduleView.as_view(),
        name='update-schedule'

    ),
    path(
        '<counseling_schedule_id>/delete',
        views.DeleteCounsellorScheduleView.as_view(),
        name='delete-schedule'

    ),
    path(
        'booking/list',
        views.ListBookingView.as_view(),
        name='list-booking'

    ),
    path(
        'booking/<booking_id>/update',
        views.UpdateBookingView.as_view(),
        name='update-booking'

    ),
    path(
        'booking/<booking_id>/delete',
        views.UpdateBookingView.as_view(),
        name='update-booking'

    )
]