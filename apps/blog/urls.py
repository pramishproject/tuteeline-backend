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
    ),
    path(
        '<str:consultancy_staff_id>/consultancy/add',
        views.CreateConsultancyBlog.as_view(),
        name='add-consultancy-blog'
    ),
    path(
        '<str:consultancy_id>/student/list',
        views.ListConsultancyBlogForStudent.as_view(),
        name="list-consultancy-student"
    ),
    path(
        '<str:consultancy_id>/consultancy/list',
        views.ListConsultancyBlog.as_view(),
        name="list-consultancy-blog"
    ),
    path(
        '<str:consultancy_blog_id>/consultancy/update',
        views.UpdateConsultancyBlog.as_view(),
        name = "update-blog-consultancy"
    ),
    path(
        '<str:consultancy_blog_id>/consultancy/delete',
        views.DeleteConsultancyBlog.as_view(),
        name="delete-consultancy-blog"
    ),
    path(
        '<str:consultancy_blog_id>/consultancy/approve',
        views.ApproveConsultancyBlog.as_view(),
        name="approve-consultancy-blog"
    )
]
