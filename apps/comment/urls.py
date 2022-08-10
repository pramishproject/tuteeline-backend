from django.urls import path

from apps.comment import views

urlpatterns = [
    path(
        '<apply_id>/application/add',
        views.AddComment.as_view(),
        name="add-comment"
         ),
    path(
        '<apply_id>/parent/application/list',
        views.ListApplicationComment.as_view(),
        name="list-comment"
    ),
    path(
        '<comment_id>/child/application/list',
        views.ListChildApplicationComment.as_view(),
        name = 'list-child-comment'
    )
]