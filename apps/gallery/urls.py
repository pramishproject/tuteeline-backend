from django.urls import path

from apps.gallery import views

urlpatterns = [
    path(
        'consultancy/add',
        views.AddConsultancyGalleryView.as_view(),
        name='add-gallery'
    ),
    path(
        '<consultancy_id>/consultancy/student/list',
        views.ListConsultancyGalleryForStudentView.as_view(),
        name='list-gallery'
    ),
    path(
        '<consultancy_id>/consultancy/list',
        views.ListConsultancyGallery.as_view(),
        name = "list-consultancy gallery"
    ),
    # path(
    #     '<str:gallery_id>/update',
    #     views.UpdateGalleryView.as_view(),
    #     name='update-gallery'
    #
    # ),
    # path(
    #     '<str:gallery_id>/delete',
    #     views.DeleteGalleryView.as_view(),
    #     name='delete-gallery'
    #
    # ),
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