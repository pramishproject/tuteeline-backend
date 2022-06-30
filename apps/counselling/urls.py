from django.urls import path

from apps.counselling import views

urlpatterns =[
    path(
        "<str:student_id>/apply_institute_counceling",
        views.CreateInstituteCounselling.as_view(),
        name="institute-counselling"
    ),
    path(
        "<str:student_id>/student_councelling_list",
        views.StudentCounsellingList.as_view(),
        name="counselling-list"
    ),
    path(
        "<str:institute_id>/institute/counselling/list",
        views.StudentCounsellingListForInstitute.as_view(),
        name="institute-counselling-list"
    ),
    path(
        "<str:counselling_id>/institute/Assign",
        views.AssignCounsellingStudent.as_view(),
        name="assign"
    ),
    path(
        "<str:counselling_id>/institute/notes",
        views.AddNotesView.as_view(),
        name="add-notes"
    ),
    path(
        "<str:institute_staff_id>/institute/staff/list",
        views.AssignCouncilingListView.as_view(),
        name="list-assign-counselling"
    ),
    path(
        "<str:student_id>/consultancy/add",
        views.CreateConsultancyCounselling.as_view(),
        name = "add-counseling"
    ),
    # path()

]