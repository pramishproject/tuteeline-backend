from django.urls import path

from apps.staff import views

urlpatterns = [
    path(
        'add',
        views.AddStaffPositionView.as_view(),
        name='add-staff-position',
    ),
    path(
        'list',
        views.ListStaffPositionView.as_view(),
        name='list-staff-position',
    ),
    path(
        '<str:staff_position_id>/update',
        views.UpdateInstituteStaffRole.as_view(),
        name='update-staff-position',
    ),
    path(
        '<str:staff_position_id>/delete',
        views.DeleteStaffPositionView.as_view(),
        name='delete-staff-position',
    ),
    path(
        '<institute_id>/institute/add',
        views.CreateInstituteRole.as_view(),
        name='add-institute-role'
    ),
    path(
        '<institute_id>/institute/list',
        views.ListInstituteRole.as_view(),
        name="list-institute-role"
    )

]
