from django.urls import path
from apps.linkage import views
urlpatterns = [
    path(
        'linkage/list',
        views.InstituteLinkageList.as_view(),
        name="linkage-list"
    ),
]