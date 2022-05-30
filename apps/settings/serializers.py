from rest_framework import serializers

from apps.settings.models import Settings


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'


class AddSettingColorSerializer(SettingSerializer):
    class Meta(SettingSerializer.Meta):
        fields = ('color',)


class ListSettingColorSerializer(SettingSerializer):
    class Meta(SettingSerializer.Meta):
        fields = (
            'id',
            'color',
            'created_at',
        )


class UpdateColorSerializer(AddSettingColorSerializer):
    pass
