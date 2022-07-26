from django.urls import path
from apps.role import views
urlpatterns = [
    path(
        '<institute_id>/institute/add',
        views.CreateInstituteRole.as_view(),
        name='add-institute-role'
    ),
]