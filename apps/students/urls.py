from django.urls import path

from apps.students import views
# from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path(
        'register',
        views.RegisterStudentView.as_view(),
        name='register-institute'
    ),
    path(
        'init/<student_id>/student-profile',
        views.StudentInitProfileView.as_view(),
        name='student-init-view'
    ),
    path(
        '<student_id>/detail',
        views.GetStudentDetailView.as_view(),
        name="student-detail"
    ),
    path(
        '<student_id>/student-address',
        views.StudentAddressView.as_view(),
        name = 'student address view'
    ),
    path(
        '<student_id>/update',
        views.UpdateStudentView.as_view(),
        name = 'student-update-view'
    ),
    path(
        '<student_id>/update/profile',
        views.UpdateImageView.as_view(),
        name = 'student-profile-update'
    ),
    path(
        '<address_id>/update/address',
        views.StudentAddressUpdateView.as_view(),
        name = 'student-profile-update'
    ),
    path(
        '<student_id>/get/address',
        views.GetStudentAddressView.as_view(),
        name= 'get-student-address'
    ),
    path(
        '<student_id>/update/latlong',
        views.StudentLatitudeAndLongitudeUpdate.as_view(),
        name = 'update-latitude and longitude'
    ),
    path(
        '<student_id>/favourite/add',
        views.AddFavouriteInstitute.as_view(),
        name = 'add-fav'
    ),
    path(
        '<student_id>/favourite/get',
        views.GetFavouriteInstitute.as_view(),
        name='get-favourite'
    ),
    path(
        '<favourite_id>/favourite/delete',
        views.DeleteFavouriteInstitute.as_view(),
        name="delete-favourite"
    ),
    path(
        '<student_id>/visitor/add',
        views.CreateInstituteVisitorView.as_view(),
        name="visitor create"
    ),
    path(
        '<student_id>/visitor/list',
        views.ListVisitorHistryView.as_view(),
        name="list-visitor"
    ),
    path(
        'list',
        views.ListStudentsForPortal.as_view(),
        name = "list"
    ),
]
# urlpatterns = format_suffix_patterns (urlpatterns)

