from django.urls import path

from apps.notification import views

urlpatterns = [
    path(
        'consultancy-receive',
        views.ConsultancyReceiveNotificationView.as_view(),
        name='consultancy_receive_notification'
    ),
    path(
        'portal-receive',
        views.PortalReceiveNotificationView.as_view(),
        name='portal_receive_notification'
    ),
    path(
        'send',
        views.SendNotificationView.as_view(),
        name='send_notification'
    )
]