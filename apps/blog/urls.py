from django.urls import path

from apps.blog import views

urlpatterns = [
    path(
        'add',
        views.AddBlogsView.as_view(),
        name='add-blogs'

    ),
    path(
        'list',
        views.ListBlogsView.as_view(),
        name='list-blogs'

    ),
    path(
        '<str:blog_id>/update',
        views.UpdateBlogView.as_view(),
        name='update-blog'

    ),
    path(
        '<str:blog_id>/delete',
        views.DeleteBlogView.as_view(),
        name='delete-blog'

    ),
    path(
        'relation/add',
        views.AddRelationView.as_view(),
        name='add-relation'

    ),
    path(
        'relation/list',
        views.ListRelationView.as_view(),
        name='list-relation'

    ),
    path(
        'relation/<str:relation_id>/update',
        views.UpdateRelationView.as_view(),
        name='update-relation'

    ),
    path(
        'relation/<str:relation_id>/delete',
        views.DeleteRelationView.as_view(),
        name='delete-relation'

    ),
    path(
        'institute/<str:institute_id>/add',
        views.CreateInstituteBlogView.as_view(),
        name='create-institute'
    ),
    path(
        'institute/<str:institute_id>/list',
        views.ListInstituteBlogsView.as_view(),
        name ='list institute blog'
    ),
    path(
        'institute/<str:institute_blog_id>/update',
        views.UpdateInstituteBlogView.as_view(),
        name ='update-institute-blog'
    ),
    path(
        'institute/<str:institute_blog_id>/delete',
        views.DeleteInstituteBlogView.as_view(),
        name = 'delete-institute-blog'
    ),
    path(
        'portal/<str:staff_id>/addblog',
        views.CreatePortalBlogView.as_view(),
        name='addblog'
    )
]
