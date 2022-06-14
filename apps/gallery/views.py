from django.shortcuts import render

# Create your views here.
from apps.consultancy.mixins import ConsultancyMixin
from apps.core import generics
from apps.gallery import serializers, usecases
from apps.gallery.mixins import  InstituteGalleryMixins
from django.utils.translation import gettext_lazy as _

from apps.institute.mixins import InstituteMixins


class AddConsultancyGalleryView(generics.CreateWithMessageAPIView):
    """
    Use this end-point to add gallery
    """
    serializer_class = serializers.AddConsultancyGallerySerializer
    message = 'Created successfully'

    def perform_create(self, serializer):
        return usecases.AddConsultancyGalleryUseCase(serializer=serializer).execute()


class ListConsultancyGalleryForStudentView(generics.ListAPIView,ConsultancyMixin):
    """
    Use this end-point to List  all  blogs
    """
    serializer_class = serializers.ListConsultancyGalleryForStudentSerializer
    no_content_error_message = _('No gallery at the moment')
    def get_object(self):
        return self.get_consultancy()

    def get_queryset(self):
        return usecases.ListConsultancyGalleryUseCase(
            consultancy=self.get_object()
        ).execute()


class ListConsultancyGallery(generics.ListAPIView,ConsultancyMixin):
    serializer_class = serializers.ListConsultancyGallerySerializer
    no_content_error_message = _('No gallery at the moment')

    def get_object(self):
        return self.get_consultancy()

    def get_queryset(self):
        return usecases.ListConsultancyGalleryUseCase(
            consultancy=self.get_object()
        ).execute()


# class DeleteGalleryView(GalleryMixin, generics.DestroyAPIView):
#     """
#     Use this endpoint to delete gallery
#     """
#
#     def get_object(self):
#         return self.get_gallery()
#
#     def perform_destroy(self, instance):
#         return usecases.DeleteGalleryUseCase(
#             gallery=self.get_object(),
#         ).execute()


# class UpdateGalleryView(generics.UpdateAPIView, GalleryMixin):
#     """
#     Use this end-point to Update   blogs.
#     """
#
#     serializer_class = serializers.UpdateGallerySerializer
#     queryset = ''
#
#
#     def get_object(self):
#         return self.get_gallery()
#
#     def perform_update(self, serializer):
#         return usecases.UpdateGalleryUseCase(
#             serializer=serializer,
#             gallery=self.get_object()
#         ).execute()

class AddInstituteGalleryView(generics.CreateWithMessageAPIView,InstituteMixins):
    """
    Institute Gallery added 
    """
    serializer_class = serializers.AddInstituteGallerySerializer
    message ="add institute gallery picture successfully"

    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecases.AddInstituteGalleryUseCase(
            serializer=serializer,
            institute=self.get_object()
            ).execute()


class ListInstituteGalleryView(generics.ListAPIView,InstituteMixins):
    """
    Listed institute Gallery for institute
    """
    serializer_class = serializers.ListInstituteGallerySerializer
    message = "list institute gallery"

    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListInstituteGalleryUseCase(
            institute=self.get_object()
        ).execute()
class UpdateInstituteGalleryView(generics.UpdateWithMessageAPIView,InstituteGalleryMixins):
    """
    approve institute gallery image
    """
    serializer_class = serializers.UpdateInstituteGalleryForStudentSerializer
    message = "approve institute gallery"

    def get_object(self):
        return self.get_institute_gallery()

    def perform_update(self,serializer):
        return usecases.ApprovedInstituteGalleryUsecase(
            gallery=self.get_object(),
            serializer = serializer,
        ).execute()

class DeleteInstituteGalleryView(generics.DestroyAPIView,InstituteGalleryMixins):
    """
    delete institute 
    """
    message = "delete institute gallery"
    def get_object(self):
        return self.get_institute_gallery()

    def perform_destroy(self, instance):
        return usecases.DeleteInstituteGalleryUseCase(
            gallery=self.get_object(),
        ).execute()
        
class ApproveInstituteGalleryView(generics.UpdateWithMessageAPIView,InstituteGalleryMixins):
    """
    approve institute gallery image
    """
    serializer_class = serializers.ApproveInstituteGallerySerializer
    message = "approve institute gallery"

    def get_object(self):
        return self.get_institute_gallery()

    def perform_update(self,serializer):
        return usecases.ApprovedInstituteGalleryUsecase(
            gallery=self.get_object(),
            serializer = serializer,
        ).execute()

class InstituteGalleryListForStudentView(generics.ListAPIView,InstituteMixins):
    """
    Listed institute Gallery for student
    """
    serializer_class = serializers.ListInstituteGalleryForStudentSerializer
    message = "list institute gallery"

    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListInstituteGalleryUseCase(
            institute=self.get_object()
        ).execute()
