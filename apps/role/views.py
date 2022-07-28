from apps.core import generics
from apps.institute.mixins import InstituteMixins
from apps.role import usecases
from apps.role import serializers
class CreateInstituteRole(generics.CreateAPIView,InstituteMixins):
    """
    this api is use to create institute role
    """
    serializer_class = serializers.AddInstituteRoleSerializers
    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecases.CreateRoleUseCases(
            serializers=serializer,
            institute=self.get_queryset(),
        ).execute()

class ListInstituteRole(generics.ListAPIView,InstituteMixins):
    """list role"""
    serializer_class = serializers.InstituteRoleListSerializers
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListInstituteRoleUseCase(
            institute=self.get_object()
        ).execute()