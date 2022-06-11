from apps.core import generics

# Create your views here.
from apps.institute.mixins import InstituteMixins
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from apps.linkage import usecases
from apps.linkage import serializers

class LinkageInstituteAndConsultancy(generics.CreateWithMessageAPIView): #TODO create linkage
    pass

class GetLinkageConsultancy(generics.ListAPIView): #TODO list linkage
    pass

class LinkageGrantedByAdmin(generics.UpdateWithMessageAPIView): #TODO status change
    pass

class InstituteLinkageList(generics.ListAPIView):
    "this endpoint is use to list "
    serializer_class = serializers.InstituteLinkageListSerializer
    no_content_error_message = _('No gallery at the moment')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['institute']
    def get_queryset(self):
        return usecases.ListInstituteLinkageConsultancyUseCase().execute()
