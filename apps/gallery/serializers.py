from rest_framework import serializers

from apps.gallery.models import Gallery, InstituteGallery


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class AddGallerySerializer(GallerySerializer):
    class Meta(GallerySerializer.Meta):
        fields = (
            'image',
            'title'

        )


class ListGallerySerializer(GallerySerializer):
    class Meta(GallerySerializer.Meta):
        fields = (
            'id',
            'image',
            'title',
            'created_at',
            'updated_at',
        )


class UpdateGallerySerializer(AddGallerySerializer):
    pass


class AddInstituteGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteGallery
        fields = (
            'title', 
            'image', 
            'uploaded_image',)

class ListInstituteGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteGallery
        fields = ('__all__')

class ApproveInstituteGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteGallery
        fields = (
            'approve',
            )

class ListInstituteGalleryForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteGallery
        fields = (
            'title', 
            'image',
        )

class UpdateInstituteGalleryForStudentSerializer(ListInstituteGalleryForStudentSerializer):
    pass
