from apps.core.usecases import BaseUseCase
from apps.institute.models import Institute
from apps.role.exceptions import PermissionFormatError, UnKnownPermissionType
from apps.role.models import Role,INSTITUTE_PERMISSIONS

class CreateRoleUseCases(BaseUseCase):
    def __init__(self,institute:Institute,serializers):
        self._institute = institute
        self._serializers = serializers
        self._data = self._serializers.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        permissions = self._data.get("permissions")
        name = self._data.get("name")
        if not isinstance(permissions, list):
            raise PermissionFormatError
        else:
            permissions = set(permissions)
            for i in permissions:
                if i not in INSTITUTE_PERMISSIONS:
                    raise UnKnownPermissionType

        Role.objects.create(
            name=name,
            permissions=list(permissions),
            institute=self._institute
            )

class ListInstituteRoleUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._role

    def _factory(self):
        self._role = Role.objects.filter(institute=self._institute)