from apps.blog.serializers import ListConsultancyBlog
from apps.consultancy.mixins import ConsultancyMixin, ConsultancyStaffMixin
from apps.institute.mixins import InstituteMixins
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny
from apps.blog import serializers, usecases
from apps.blog.mixins import BlogsMixin, InstituteBlogMixin, RelationMixin, ConsultancyBlogMixin
from apps.core import generics
from apps.portal.mixins import PortalStaffUserMixin
from apps.utils.currency import RealTimeCurrencyConverter

class AddBlogsView(generics.CreateWithMessageAPIView):
    """
    Use this end-point to add blogs
    """
    serializer_class = serializers.AddBlogSerializer
    message = 'Created successfully'

    def perform_create(self, serializer):
        return usecases.AddBlogUseCase(serializer=serializer).execute()


class ListBlogsView(generics.ListAPIView):
    """
    Use this end-point to List  all  blogs
    """
    serializer_class = serializers.ListBlogSerializer
    no_content_error_message = _('No blogs at the moment')

    def get_queryset(self):
        return usecases.ListBlogsUseCase().execute()


class DeleteBlogView(BlogsMixin, generics.DestroyAPIView):
    """
    Use this endpoint to delete blogs
    """

    def get_object(self):
        return self.get_blogs()

    def perform_destroy(self, instance):
        return usecases.DeleteBlogUseCase(
            blogs=self.get_object(),
        ).execute()


class UpdateBlogView(generics.UpdateAPIView, BlogsMixin):
    """
    Use this end-point to Update   blogs.
    """

    serializer_class = serializers.UpdateBlogSerializer
    queryset = ''

    # permission_classes = (IsAdminUser,)

    def get_object(self):
        return self.get_blogs()

    def perform_update(self, serializer):
        return usecases.UpdateBlogsUseCase(
            serializer=serializer,
            blogs=self.get_object()
        ).execute()


class AddRelationView(generics.CreateWithMessageAPIView):
    """
    Use this end-point to add relation
    """
    serializer_class = serializers.AddRelationSerializer
    message = 'Created successfully'

    def perform_create(self, serializer):
        return usecases.AddRelationUseCase(serializer=serializer).execute()


class ListRelationView(generics.ListAPIView):
    """
    Use this end-point to List  all  relation
    """
    serializer_class = serializers.ListRelationSerializer
    no_content_error_message = _('No relation at the moment')

    def get_queryset(self):
        return usecases.ListRelationUseCase().execute()


class DeleteRelationView(RelationMixin, generics.DestroyAPIView):
    """
    Use this endpoint to delete relation
    """

    def get_object(self):
        return self.get_relation()

    def perform_destroy(self, instance):
        return usecases.DeleteRelationUseCase(
            relation=self.get_object(),
        ).execute()


class UpdateRelationView(generics.UpdateAPIView, RelationMixin):
    """
    Use this end-point to Update   relations.
    """

    serializer_class = serializers.UpdateRelationSerialzier
    queryset = ''

    # permission_classes = (IsAdminUser,)

    def get_object(self):
        return self.get_relation()

    def perform_update(self, serializer):
        return usecases.UpdateRelationUseCase(
            serializer=serializer,
            relation=self.get_object()
        ).execute()

# class Get

class CreateInstituteBlogView(generics.CreateWithMessageAPIView,InstituteMixins):
    """
    This endpoint is use to create institute blog
    """
    serializer_class = serializers.CreateInstituteBlogSerializer
    message = _("institute blog create Successfully")

    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecases.CreateInstituteBlogUseCase(
            institute=self.get_object(),
            serializer= serializer
        ).execute()

class ListInstituteBlogsView(generics.ListAPIView,InstituteMixins):
    """
    This endpoint is use to list institute blog
    """
    serializer_class = serializers.ListInstituteBlogSerializer

    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListInstituteBlogsUseCase(
            institute=self.get_object(),
        ).execute()

class UpdateInstituteBlogView(generics.UpdateAPIView,InstituteBlogMixin):
    """
    this end point is use to update blogs
    """
    serializer_class = serializers.UpdateInstituteBlogSerializer
    message = _('Update blog Successfully')
    permission_classes = (AllowAny,)
    def get_object(self):
        return self.get_institute_blog()

    def perform_update(self, serializer):
        return usecases.InstituteBlogUpdateUseCase(
            blog=self.get_object(),
            serializer = serializer
        ).execute()

class DeleteInstituteBlogView(generics.DestroyAPIView,InstituteBlogMixin):
    """
    This endpoint is use to delete institute blog
    """
    def get_object(self):
        return self.get_institute_blog()

    def perform_destroy(self, instance):
        return usecases.DeleteInstituteBlogUseCase(
            blog=self.get_object(),
        ).execute()


class CreatePortalBlogView(generics.CreateWithMessageAPIView,PortalStaffUserMixin):
    """
    This endpoint is use to create portal blog
    """
    serializer_class = serializers.CreatePortalUserBlogSerializer
    message = _('Update blog Successfully')
    permission_classes = (AllowAny,)
    def get_object(self):
        return self.get_portal_staff()

    def perform_create(self, serializer):
        usecases.AddBlogPortalUseCase(
            user=self.get_object(),
            serializer=serializer,
        ).execute()


# ----------------------------------Start Consultancy---------------------------

class CreateConsultancyBlog(generics.CreateWithMessageAPIView,ConsultancyStaffMixin):
    """
    This api is use to create consultancy blog
    """
    serializer_class = serializers.CreateConsultancyBlogSerializer
    message = _("Consultancy Blog Create Successfully")
    def get_object(self):
        return self.get_consultancy_staff()

    def perform_create(self, serializer):
        usecases.CreateConsultancyBlogUseCase(
            staff=self.get_object(),
            serializer=serializer,
        ).execute()

class ListConsultancyBlog(generics.ListAPIView,ConsultancyMixin):
    """
    This api is list blog
    """
    serializer_class = ListConsultancyBlog
    def get_object(self):
        return self.get_consultancy()

    def get_queryset(self):
        return usecases.ListConsultancyBlog(
            consultancy=self.get_object(),
        ).execute()

class ListConsultancyBlogForStudent(generics.ListAPIView,ConsultancyMixin):
    """
    list consultancy blog for student
    """
    serializer_class = serializers.ListConsultancyBlogForStudentSerializer

    def get_object(self):
        return self.get_consultancy()

    def get_queryset(self):
        return usecases.ListConsultancyBlog(
            consultancy=self.get_object(),
        ).execute()

class UpdateConsultancyBlog(generics.UpdateWithMessageAPIView,ConsultancyBlogMixin):
    """
    update consultancy blog
    """
    serializer_class = serializers.UpdateConsultancyBlogSerializer
    def get_object(self):
        return self.get_consultancy_blog()

    def perform_update(self, serializer):
        usecases.UpdateConsultancyBlogUseCase(
            blogs=self.get_object(),
            serializer = serializer,
        ).execute()

class ApproveConsultancyBlog(generics.UpdateWithMessageAPIView,ConsultancyBlogMixin):
    serializer_class = serializers.ApproveConsultancyBlogSerializer
    def get_object(self):
        return self.get_consultancy_blog()

    def perform_update(self, serializer):
        usecases.UpdateConsultancyBlogUseCase(
            blogs=self.get_object(),
            serializer = serializer,
        ).execute()


class DeleteConsultancyBlog(generics.DestroyWithMessageAPIView,ConsultancyBlogMixin):
    """
    delete
    """
    def get_object(self):
        return self.get_consultancy_blog()

    def perform_destroy(self, instance):
        usecases.DeleteConsultancyBlogUseCase(
            blogs=self.get_object()
        ).execute()
# ----------------------------------end Consultancy---------------------------