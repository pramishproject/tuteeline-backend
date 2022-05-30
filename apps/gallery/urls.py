from django.urls import path

from apps.gallery import views

urlpatterns = [
    path(
        'add',
        views.AddGalleryView.as_view(),
        name='add-gallery'
    ),
    path(
        'list',
        views.ListGalleryView.as_view(),
        name='list-gallery'
    ),
    path(
        '<str:gallery_id>/update',
        views.UpdateGalleryView.as_view(),
        name='update-gallery'

    ),
    path(
        '<str:gallery_id>/delete',
        views.DeleteGalleryView.as_view(),
        name='delete-gallery'

    ),
    path(
        '<str:institute_id>/institute/add',
        views.AddInstituteGalleryView.as_view(),
        name='add-institute-gallery'
    ),
    path(
        '<str:institute_id>/institute/list',
        views.ListInstituteGalleryView.as_view(),
        name="list institute gallery"
    ),
    path(
        '<str:institute_id>/institute/list',
        views.ListInstituteGalleryView.as_view(),
        name="list institute gallery"
    ),
    path(
        '<str:institute_gallery_id>/institute/delete',
        views.DeleteInstituteGalleryView.as_view(),
        name = "delete institute gallery"
    ),
    path(
        '<str:institute_gallery_id>/institute/approve',
        views.ApproveInstituteGalleryView.as_view(),
        name="approve institute gallery"
    ),
    path(
        '<str:institute_id>/institute/student/list',
        views.InstituteGalleryListForStudentView.as_view(),
        name="list institute gallery"
    ),
    path(
        '<str:institute_gallery_id>/institute/update',
        views.UpdateInstituteGalleryView.as_view(),
        name = "update institute gallery"
    ),
]