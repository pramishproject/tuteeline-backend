from django.urls import path

from apps.parentsDetail import views

urlpatterns = [
    path(
        '<student_id>/add',
        views.AddParentsView.as_view(),
        name="add-student-parents-detail"
    ),
    path(
        '<student_id>/parents/list',
        views.GetParentsView.as_view(),
        name = "get-parents-detail"
    ),
    path(
        '<parents_id>/parents/update',
        views.UpdateParentsView.as_view(),
        name= "update-parents-view"
    )
]
