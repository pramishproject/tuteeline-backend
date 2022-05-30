from django.urls import path
from apps.studentIdentity import views

urlpatterns = [
    path(
        '<student_id>/citizenship/add',
        views.AddCitizenshipView.as_view(),
        name = 'add-citizenship'
    ),
    path(
        '<student_id>/passport/add',
        views.AddPassportView.as_view(),
        name = 'add-passport'
    ),
    path(
        'passport/<student_id>/get',
        views.GetPassportView.as_view(),
        name= 'get-passport'
    ),
    path(
        '<student_id>/citizenship/get',
        views.GetCitizenshipView.as_view(),
        name='get-passport'
    ),
    path(
        '<student_id>/citizenship/frontimage/update',
        views.UpdateCitizenshipFrontPageView.as_view(),
        name = "update-citizenship"
    ),
    path(
        '<student_id>/citizenship/backimage/update',
        views.UpdateCitizenshipBackPageView.as_view(),
        name = 'Update-citizenship-back'
    ),
    path(
        '<student_id>/citizenship/update',
        views.UpdateCitizenshipView.as_view(),
        name = "update-citizenship"
    ),
    path(
        '<student_id>/passport/image/update',
        views.UpdatePassportImageView.as_view(),
        name = "update-passport"
    ),
    path(
        '<student_id>/passport/update',
        views.UpdatePassportView.as_view(),
        name = "update-passport"
    )
    # UpdatePassportView
]
