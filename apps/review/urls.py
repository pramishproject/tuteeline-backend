from django.urls import path
from rest_framework import urlpatterns

from apps.review import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(
        '<student_id>/institute/add',
        views.CreateInstituteReviewView.as_view(),
        name="create institute review"
        ),
    path('<institute_review_id>/institute/update',
        views.UpdateInstituteReviewView.as_view(),
        name="update institute review"
        ),
    path('<institute_id>/institute/list',
        views.ListInstituteReviewView.as_view(),
        name="list institute"
    )
]