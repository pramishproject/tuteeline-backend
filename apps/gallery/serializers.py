from rest_framework import serializers

from apps.gallery.models import InstituteGallery, ConsultancyGallery


class ConsultancyGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyGallery
        fields = '__all__'


class AddConsultancyGallerySerializer(ConsultancyGallerySerializer):
    class Meta(ConsultancyGallerySerializer.Meta):
        fields = (
            'image',
            'title',
            'consultancy',
            'uploaded_image'
        )

class ListConsultancyGallerySerializer(ConsultancyGallerySerializer):
    pass

class ListConsultancyGalleryForStudentSerializer(ConsultancyGallerySerializer):
    class Meta(ConsultancyGallerySerializer.Meta):
        fields = (
            'id',
            'image',
            'title',
            'created_at',
            'updated_at',
        )


# class UpdateGallerySerializer(AddGallerySerializer):
#     pass


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
