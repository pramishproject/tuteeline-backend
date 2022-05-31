from django.urls import path

from apps.counselling import views

urlpatterns =[
    path(
        "<str:student_id>/apply_institute_counceling",
        views.CreateInstituteCounselling.as_view(),
        name="institute counselling"
    ),

]