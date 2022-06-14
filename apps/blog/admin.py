from django.contrib import admin

# Register your models here.
from apps.blog.models import Blogs,Relation,InstituteBlog,ConsultancyBlog
from apps.core.admin import BaseModelAdmin


@admin.register(Relation)
class RelationAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display+(
        'name',
    )

@admin.register(Blogs)
class BlogAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display+(
        'title',
        'relation',
        'author_name'
    )

@admin.register(InstituteBlog)
class InstituteBlogAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'title',
        'relation',
        'author_name',
        'institute',
    )

@admin.register(ConsultancyBlog)
class ConsultancyBlogAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'title',
        'relation',
        'author_name',
        'consultancy',
    )