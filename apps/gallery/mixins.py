from apps.gallery.usecases import GetGalleryUseCase,GetInstituteGalleryUseCase


class GalleryMixin:
    def get_gallery(self):
        return GetGalleryUseCase(
            gallery_id=self.kwargs.get('gallery_id')
        ).execute()


class InstituteGalleryMixins:
    def get_institute_gallery(self):
        return GetInstituteGalleryUseCase(
            gallery =self.kwargs.get('institute_gallery_id')
        ).execute()
