from rest_framework import serializers

from apps.role.models import Role


class AddInstituteRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'name',
            'permissions',
        )

class InstituteRoleListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'permissions',
            'created_at' ,
            'updated_at',
        )