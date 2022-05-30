from django.urls import path
from rest_framework import urlpatterns

from apps.language import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(
        '<student_id>/create',
        views.CreateLanguageView.as_view(),
        name="create-language-view"
        ),

    path(
        '<student_id>/get',
        views.GetLanguageView.as_view(),
        name='get-language-view'
    ),
    path(
        '<language_id>/update',
        views.UpdateLanguageView.as_view(),
        name = 'update-language-view'
    ),
    path(
        '<language_id>/delete',
        views.DeleteLanguageView.as_view(),
        name = 'delete language'
    )
]