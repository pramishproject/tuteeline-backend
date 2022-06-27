from apps.consultancy.mixins import ConsultancyMixin
from apps.core import generics

# Create your views here.
from apps.institute.mixins import InstituteMixins
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from apps.linkage import usecases
from apps.linkage import serializers
from apps.linkage.serializers import CreateLinkageSerializer


class LinkageInstituteAndConsultancy(generics.CreateAPIView,ConsultancyMixin): #TODO create linkage
    serializer_class = CreateLinkageSerializer

    def get_object(self):
        return self.get_consultancy()

    def perform_create(self, serializer):
        return usecases.CreateLinkageUseCase(
            consultancy=self.get_object(),
            serializer = serializer
        )

class GetLinkageConsultancy(generics.ListAPIView): #TODO list linkage
    pass

class LinkageGrantedByAdmin(generics.UpdateWithMessageAPIView): #TODO status change
    pass

class InstituteLinkageList(generics.ListAPIView):
    "this endpoint is use to list "
    serializer_class = serializers.InstituteLinkageListSerializer
    no_content_error_message = _('No Linkage at the moment')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['institute']
    def get_queryset(self):
        return usecases.ListInstituteLinkageConsultancyUseCase().execute()



