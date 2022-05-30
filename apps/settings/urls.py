from django.urls import path
from apps.settings import views

urlpatterns = [
    path(
        'add-color',
        views.AddColorView.as_view()
         ),
    path(
        'list-color',
        views.ListSettingColorView.as_view()
         ),
    path(
        '<setting_id>/update-color',
        views.UpdateSettingColorView.as_view()
    ),
    # path(
    #     '<setting_id>/delete-color',
    #     views.DeleteSettingColorView.as_view()
    # )
]