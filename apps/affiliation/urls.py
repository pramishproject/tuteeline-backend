from django.urls import path

from apps.affiliation import views

urlpatterns = [
    path(
        'institute/<str:institute_id>/add',
        views.AddAffiliation.as_view(),
        name='add-affiliation'
    ),
    path(
        'institute/<str:institute_id>/institute/list',
        views.ListOfAffiliation.as_view(),
        name="list-affiliation-institute"
    )
    ]