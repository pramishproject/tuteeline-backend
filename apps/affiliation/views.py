from django.shortcuts import render
from apps.core import generics
# Create your views here.
from apps.institute.mixins import InstituteMixins
from apps.affiliation import usecases,serializers

class AddAffiliation(generics.CreateAPIView,InstituteMixins):
    serializer_class = serializers.AddAffiliationSerializer
    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecases.AddAffiliationUseCase(
            institute=self.get_object(),
            serializer=serializer,
        ).execute()

