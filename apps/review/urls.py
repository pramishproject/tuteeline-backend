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
    ),
    path(
        '<institute_id>/institute/aggregate',
        views.GetInstituteAggregateReviewView.as_view(),
        name = "institute-aggregate-review"
    ),
    path(
        '<student_id>/consultancy/add',
        views.CreateConsultancyReviewView.as_view(),
        name="consultancy-review-add"
    ),
    path(
        '<consultancy_id>/consultancy/list',
        views.ListConsultancyReview.as_view(),
        name="consultancy-list"
    ),
    path(
        '<consultancy_review_id>/consultancy/update',
        views.UpdateConsultancyReview.as_view(),
        name="update-consultancy"
    )
]