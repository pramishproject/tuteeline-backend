from django.shortcuts import render
from apps.core import generics
# Create your views here.
from apps.institute.mixins import InstituteMixins
from apps.affiliation import usecases,serializers

class AddAffiliation(generics.CreateAPIView,InstituteMixins):
    """
    course:{type:"ALL or CUSTOM",course:[name:"","id":"course_id"]} if All
    """
    serializer_class = serializers.AddAffiliationSerializer
    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecases.AddAffiliationUseCase(
            institute=self.get_object(),
            serializer=serializer,
        ).execute()


class ListOfAffiliation(generics.ListAPIView,InstituteMixins):
    serializer_class = serializers.ListOfAffiliation
    def get_object(self):
        return self.get_institute()
    def get_queryset(self):
        return usecases.ListAffiliation(institute=self.get_object()).execute()