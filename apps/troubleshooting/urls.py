from django.urls import path

from apps.troubleshooting import views

urlpatterns = [
    path(
        'counsultancy-staff/<str:consultancy_staff_id>/add',
        views.AddTroubleShootTicketView.as_view(),
        name='add-troubleshot'
    ),
    path(
        'list',
        views.ListTroubleShootTicketView.as_view(),
        name='list-troubleshot'
    ),
    path(
        '<str:troubleshoot_id>/update',
        views.UpdateTroubleShootStatusView.as_view(),
        name='update-troubleshot'
    )
]
