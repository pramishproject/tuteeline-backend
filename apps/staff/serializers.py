from rest_framework import serializers

from apps.staff.models import StaffPosition,RoleBase


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







class AddInstituteRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = StaffPosition
        fields = (
            'name',
            'permission_list',
        )

class InstituteRoleListSerializers(serializers.ModelSerializer):
    class Meta:
        model = StaffPosition
        fields = (
            'id',
            'name',
            'permission_list',
            'created_at' ,
            'updated_at',
        )

