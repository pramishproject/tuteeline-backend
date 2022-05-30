from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.core.serializers import IdNameSerializer
from apps.user.models import NormalUser


class NormalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = '__all__'


class NormalUserProfileSerializer(NormalUserSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    fullname = serializers.CharField(source='user.fullname')
    contact_number = serializers.CharField(source='user.contact_number')
    city = IdNameSerializer()
    country = serializers.SerializerMethodField()
    available_balance = serializers.IntegerField(default=500)

    class Meta(NormalUserSerializer.Meta):
        fields = (
            'id',
            'username',
            'email',
            'avatar',
            'fullname',
            'contact_number',
            'city',
            'country',
            'description',
            'date_of_birth',
            'available_balance'
        )

    @swagger_serializer_method(serializer_or_field=IdNameSerializer())
    def get_country(self, instance):
        if instance.city:
            return IdNameSerializer(instance.city.country).data
        return None


class UpdateNormalUserProfileSerializer(NormalUserSerializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    contact_number = serializers.CharField()

    class Meta(NormalUserSerializer.Meta):
        fields = (
            'email',
            'avatar',
            'fullname',
            'contact_number',
            'city',
            'date_of_birth',
            'description',
        )


class ListNormalUserForNormalUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField(source='user.username')
