from django.utils.datetime_safe import datetime
from rest_framework.exceptions import ValidationError

from apps.core.usecases import BaseUseCase
from apps.gallery.models import InstituteGallery, ConsultancyGallery

from  django.utils.translation import  gettext_lazy as _

class AddConsultancyGalleryUseCase(BaseUseCase):
    def __init__(self,
                 serializer):
        self.serializer = serializer
        self.data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._gallery = ConsultancyGallery(**self.data)
        self._gallery.save()


class ListConsultancyGalleryUseCase(BaseUseCase):
    def __init__(self,consultancy):
        self._consultancy = consultancy
    def execute(self):
        self._factory()
        return self._gallery

    def _factory(self):
        self._gallery = ConsultancyGallery.objects.filter(consultancy=self._consultancy)


# class GetGalleryUseCase(BaseUseCase):
#     def __init__(self, gallery_id):
#         self._gallery_id = gallery_id
#
#     def execute(self):
#         self._factory()
#         return self.gallery
#
#     def _factory(self):
#         try:
#             self.gallery = Gallery.objects.get(pk=self._gallery_id)
#         except Gallery.DoesNotExist:
#             raise ValidationError({'error': _('Gallery  does not exist for following id.')})


# class UpdateGalleryUseCase(BaseUseCase):
#     def __init__(self, serializer, gallery: Gallery):
#         self.serializer = serializer
#         self._data = serializer.validated_data
#         self._gallery = gallery
#
#     def execute(self):
#         self._factory()
#
#     def _factory(self):
#         for key in self._data.keys():
#             setattr(self._gallery, key, self._data.get(key))
#         self._gallery.updated_at = datetime.now()
#         self._gallery.save()


# class DeleteGalleryUseCase(BaseUseCase):
#     def __init__(self, gallery):
#         self._gallery = gallery
#
#     def execute(self):
#         self._factory()
#
#     def _factory(self):
#         self._gallery.delete()

class AddInstituteGalleryUseCase(BaseUseCase):
    def __init__(self, institute,serializer):
        self._institute = institute
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        print(self._data.get("uploaded_image"))
        InstituteGallery.objects.create(
            institute=self._institute,
            **self._data
        )

class ListInstituteGalleryUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._gallery 

    def _factory(self):
        self._gallery=InstituteGallery.objects.filter(institute= self._institute)


class ApprovedInstituteGalleryUsecase(BaseUseCase):
    def __init__(self,gallery,serializer):
        self._gallery = gallery
        self._data = serializer.validated_data

    def execute(self):
        self._factory()
    
    def _factory(self):
        for key in self._data.keys():
            setattr(self._gallery, key, self._data.get(key))
        self._gallery.updated_at = datetime.now()
        self._gallery.save()

class GetInstituteGalleryUseCase(BaseUseCase):
    def __init__(self,gallery):
        self._gallery = gallery

    def execute(self):
        self._factory()
        return self._institute_gallery

    def _factory(self):
        try:
            self._institute_gallery = InstituteGallery.objects.get(pk=self._gallery)
        except Gallery.DoesNotExist:
            raise ValidationError({'error': _('Gallery  does not exist for following id.')})


class DeleteInstituteGalleryUseCase(BaseUseCase):
    def __init__(self,gallery):
        self._gallery = gallery

    def execute(self):
        self._factory()

    def _factory(self):
        self._gallery.delete()
