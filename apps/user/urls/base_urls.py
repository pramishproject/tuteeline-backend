from django.urls import path, include

urlpatterns = [
    path(
        'normal-user/',
        include('apps.user.urls.normal_user_urls')
    )
]
