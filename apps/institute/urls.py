from apps.institute.usecase import UpdateInstituteUseCase
from django.urls import path
from apps.institute import views

from apps.institute.views import RegisterInstituteView, UpdateInstituteView

urlpatterns = [
    path(
        'register',
        views.RegisterInstituteView.as_view(),
        name='register-institute'
    ),
    path(
        'inistitutelist',
        views.ListInstituteView.as_view(),
        name = 'institute-list'
    ),
    path(
        '<institute_id>/detail/student',
        views.DetailInstituteView.as_view(),
        name = 'institute-detail'
    ),
    path(
        '<institute_id>/update/logo',
        views.UpdateInstituteLogoView.as_view(),
        name="logo update"
    ),
    path(
        '<institute_id>/update/coverimage',
        views.UpdateInstituteCoverimageView.as_view(),
        name="coverimage update"
    ),
    path(
        '<institute_id>/update',
        views.UpdateInstituteView.as_view(),
        name = 'update'
    ),
    path(
        '<institute_id>/staff/add',
        views.AddInstituteStaffView.as_view(),
        name="add-staff"
    ),
    path(
        '<institute_id>/scholorship/add',
        views.AddScholorshipView.as_view(),
        name = 'scholorship-add'
    ),
    path(
        '<institute_id>/scholorship/list',
        views.GetScholorshipListView.as_view(),
        name = 'scholorship-list'
    ),
    path(
        '<scholorship_id>/scholorship/update',
        views.UpdateScholorshipView.as_view(),
        name = 'scholorship-update'
    ),
    path(
        '<scholorship_id>/scholorship/delete',
        views.DeleteScholorshipView.as_view(),
        name= 'delete-scholorship-view'
    ),
    path(
        '<institute_id>/staff/add',
        views.AddInstituteStaffView.as_view(),
        name='add-staff'
    ),
    path(
        '<institute_id>/socialmedia/add',
        views.AddSolicalMediaView.as_view(),
        name = 'add-social-media'
    ),
    path(
        '<socialmedia_id>/socialmedia/delete',
        views.DeleteSocialMediaView.as_view(),
        name="delete-social-media"
    ),
    path(
        '<institute_id>/socialmedia/list',
        views.GetSocialMediaListView.as_view(),
        name = 'get-social-media-list'
    ),
    path(
        '<institute_id>/addfacility',
        views.AddFacilityView.as_view(),
        name = 'add-facility'
    ),
    path(
        '<institute_id>/facility/get',
        views.GetFacilityView.as_view(),
        name = 'get-facility-view'
    ),
    path(
        '<institute_id>/staff/list',
        views.ListInstituteStaffView.as_view(),
        name = 'list-staff'
    ),
    # path( #todo
    #     '<staff_id>/staff/role/update',
    #
    # )


]
