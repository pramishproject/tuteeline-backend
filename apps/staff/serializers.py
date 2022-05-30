from rest_framework import serializers

from apps.staff.models import StaffPosition


class StaffPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPosition
        fields = '__all__'


class AddStaffPositionSerializer(StaffPositionSerializer):
    class Meta(StaffPositionSerializer.Meta):
        fields = (
            'name',
        )


class ListStaffPositionSerializer(StaffPositionSerializer):
    class Meta(StaffPositionSerializer.Meta):
        fields = (
            'id',
            'name',
            'created_at',
        )


class UpdateStaffPositionSerializer(StaffPositionSerializer):
    class Meta(StaffPositionSerializer.Meta):
        fields = (
            'name',
        )


