from django.urls import path

from apps.user.views import normal_user_views

urlpatterns = [
    path(
        'list',
        normal_user_views.ListNormalUserView.as_view(),
        name='list-normal-user'
    )
]
