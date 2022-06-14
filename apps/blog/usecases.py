from django.utils.datetime_safe import datetime
from rest_framework.exceptions import ValidationError

from apps.blog.models import Blogs, InstituteBlog, PortalBlog, Relation, ConsultancyBlog
from apps.core.usecases import BaseUseCase

from django.utils.translation import gettext_lazy as _


class AddBlogUseCase(BaseUseCase):
    def __init__(self,
                 serializer):
        self.serializer = serializer
        self.data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._blog = Blogs(**self.data)
        self._blog.save()


class ListBlogsUseCase(BaseUseCase):

    def execute(self):
        self._factory()
        return self._blogs

    def _factory(self):
        self._blogs = Blogs.objects.all()


class GetBlogsUseCase(BaseUseCase):
    def __init__(self, blog_id):
        self._blog_id = blog_id

    def execute(self):
        self._factory()
        return self._blog

    def _factory(self):
        try:
            self._blog = Blogs.objects.get(pk=self._blog_id)
        except Blogs.DoesNotExist:
            raise ValidationError({'error': _('Blogs  does not exist for following id.')})

class GetInstituteBlogsByIdUseCase(BaseUseCase):
    def __init__(self, institute_blog_id):
        self._blog_id = institute_blog_id

    def execute(self):
        self._factory()
        return self._blog

    def _factory(self):
        try:
            self._blog = InstituteBlog.objects.get(pk=self._blog_id)

        except Blogs.DoesNotExist:
            raise ValidationError({'error': _('Blogs  does not exist for following id.')})


class UpdateBlogsUseCase(BaseUseCase):
    def __init__(self, serializer, blogs: Blogs):
        self.serializer = serializer
        self._data = serializer.validated_data
        self._blogs = blogs

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._blogs, key, self._data.get(key))
        self._blogs.updated_at = datetime.now()
        self._blogs.save()


class DeleteBlogUseCase(BaseUseCase):
    def __init__(self, blogs):
        self._blogs = blogs

    def execute(self):
        self._factory()

    def _factory(self):
        self._blogs.delete()


class AddRelationUseCase(BaseUseCase):
    def __init__(self,
                 serializer):
        self.serializer = serializer
        self.data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._relation = Relation(**self.data)
        print(self._relation)
        self._relation.save()


class ListRelationUseCase(BaseUseCase):

    def execute(self):
        self._factory()
        return self._relation

    def _factory(self):
        self._relation = Relation.objects.all()


class GetRelationUseCase(BaseUseCase):
    def __init__(self, relation_id):
        self._relation_id = relation_id

    def execute(self):
        self._factory()
        return self.relation

    def _factory(self):
        try:
            self.relation = Relation.objects.get(pk=self._relation_id)
        except Relation.DoesNotExist:
            raise ValidationError({'error': _('Relation  does not exist for following id.')})


class GetConsultancyUseCase(BaseUseCase):
    def __init__(self,consultancy_blog_id):
        self._blog_id = consultancy_blog_id

    def execute(self):
        self._factory()
        return self._blog

    def _factory(self):
        try:
            self._blog = ConsultancyBlog.objects.get(pk=self._blog_id)
        except ConsultancyBlog.DoesNotExist:
            raise ValidationError({'error': _('Blog  does not exist for following id.')})

class UpdateRelationUseCase(BaseUseCase):
    def __init__(self, serializer, relation: Relation):
        self.serializer = serializer
        self._data = serializer.validated_data
        self._relation = relation

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._relation, key, self._data.get(key))
        self._relation.updated_at = datetime.now()
        self._relation.save()


class DeleteRelationUseCase(BaseUseCase):
    def __init__(self, relation):
        self._relation = relation

    def execute(self):
        self._factory()

    def _factory(self):
        self._relation.delete()

class CreateInstituteBlogUseCase(BaseUseCase):
    def __init__(self,institute,serializer):
        self._institute = institute
        self.serializer = serializer
        self.data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._blog = InstituteBlog(**self.data,institute=self._institute)
        self._blog.save()

class ListInstituteBlogsUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute =institute
    
    def execute(self):
        self._factory()
        return self._blogs

    def _factory(self):
        self._blogs = InstituteBlog.objects.filter(institute= self._institute)


class InstituteBlogUpdateUseCase(BaseUseCase):
    def __init__(self,blog:InstituteBlog,serializer):
        self._blog =blog
        self._serializer = serializer
        self._data = self._serializer.validated_data
    
    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._blog, key, self._data.get(key))
        self._blog.updated_at = datetime.now()
        self._blog.save()

class DeleteInstituteBlogUseCase(BaseUseCase):
    def __init__(self,blog:InstituteBlog):
        self._blog =blog
    def execute(self):
        self._factory()
    
    def _factory(self):
        self._blog.delete()

class GetPortalBlogByIdUseCase(BaseUseCase):
    def __init__(self,blog_id):
        self._blog_id = blog_id

    def execute(self):
        self._factory()
        return self._blog

    def _factory(self):
        try:
            self._blog = PortalBlog.objects.get(pk=self._blog_id)
        except PortalBlog.DoesNotExist:
            raise ValidationError({'error': _('Blogs  does not exist for following id.')})

class AddBlogPortalUseCase(BaseUseCase):
    def __init__(self,user,serializer):
        self._user=user
        self.serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        PortalBlog.objects.create(
            user=self._user,
            **self._data,
        )


# ------------------------- start consultancy blog--------------

class CreateConsultancyBlogUseCase(BaseUseCase):
    def __init__(self,serializer,staff):
        self._staff = staff
        self._serializer = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        ConsultancyBlog.objects.create(
            staff=self._staff,
            **self._serializer
        )

class ListConsultancyBlog(BaseUseCase):
    def __init__(self,consultancy):
        self._consultancy = consultancy

    def execute(self):
        self._factory()
        return self._blog

    def _factory(self):
        self._blog=ConsultancyBlog.objects.filter(consultancy=self._consultancy)

class UpdateConsultancyBlogUseCase(BaseUseCase):
    def __init__(self,blogs,serializer):
        self._blogs = blogs
        self.serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._blogs, key, self._data.get(key))
        self._blogs.updated_at = datetime.now()
        self._blogs.save()

class DeleteConsultancyBlogUseCase(BaseUseCase):
    def __init__(self, blogs):
        self._blogs = blogs

    def execute(self):
        self._factory()

    def _factory(self):
        self._blogs.delete()
# ------------------------- end consultancy blog ---------------