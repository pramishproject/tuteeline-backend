
from apps.institute.filter import  InstituteFilter
from apps.institute.models import Institute, InstituteStaff
from apps.institute.mixins import InstituteMixins, ScholorshipMixins, SocialMediaMixins, FacilityMixin, \
    InstituteStaffMixins
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.institute import serializers
from apps.core import generics
from apps.institute.models import Facility
from apps.institute import usecase
from rest_framework.response import Response
# Create your views here.
from apps.user.permissions import IsNormalUser, CheckPermission, IsInstituteUser
from rest_framework.views import APIView

class InitView(APIView):
    """
    init api
    """
    permission_classes = (IsAuthenticated, IsInstituteUser)
    def  get(self,request):
        user_id = self.request.user.id
        staff = InstituteStaff.objects.get(user=self.request.user)
        data = {
            "institute_id" : staff.institute.id,
            "role" : staff.role.name,
            "staff_id" : staff.id,
            "name" : self.request.user.fullname,
            "image" :staff.profile_photo.url,
            "user_id" : user_id,
            "institute_type":staff.institute.category,
            "email":staff.user.email,
            "contact":staff.contact,
            "address":staff.address,
            "permission":staff.role.permission_list
        }
        serializer = serializers.InitSerilizer(instance=data)
        data = serializer.data
        return Response(data)

class RegisterInstituteView(generics.CreateWithMessageAPIView):
    """
    use this endpoint to register consultancy
    """
    parser_classes = (MultiPartParser,FileUploadParser)
    message = _('Register successfully')
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterInstituteSerializer

    def perform_create(self, serializer):
        return usecase.RegisterInstituteUsecase(
            serializer=serializer
        ).execute()

class AddInstituteStaffView(generics.CreateWithMessageAPIView ,InstituteMixins):
    """
    This endpoint is use to add staff in institute
    """
    message = 'Institute staff create successfully'
    serializer_class = serializers.CreateInstituteStaffSerializer
    parser_classes = (MultiPartParser,FileUploadParser)
    message = _('Add staff successfully')
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecase.CreateInstituteStaffUseCase(
            institute=self.get_object(),
            serializer = serializer,
            request=self.request,
        ).execute()

class ListInstituteStaffView(generics.ListAPIView,InstituteMixins):
    """
    This endpoint is use to list institute staff
    """
    message = 'institute staff list view'
    serializer_class = serializers.InstituteStaffSerializer

    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecase.ListInstituteStaffUseCase(
            institute=self.get_object(),
        ).execute()

class GetInstituteStaffDetail(generics.RetrieveAPIView,InstituteStaffMixins):
    """staff detail"""
    serializer_class = serializers.InstituteStaffSerializer

    def get_object(self):
        return self.get_institute_staff()

    def get_queryset(self):
        return usecase.GetInstituteStaffDetailUseCase(
            staff=self.get_object()
        ).execute()

class UpdateInstituteStaffDetail(generics.UpdateWithMessageAPIView,InstituteStaffMixins):
    """Update staff"""
    serializer_class = serializers.UpdateInstituteStaffSerializer
    def get_object(self):
        return self.get_institute_staff()

    def perform_update(self, serializer):
        return usecase.InstituteStaffUpdate(
            instance=self.get_object(),
            serializer=serializer
        ).execute()

class UpdateInstituteStaffProfileImage(generics.UpdateWithMessageAPIView,InstituteStaffMixins):
    serializer_class = serializers.UpdateInstituteStaffProfileImage

    def get_object(self):
        return self.get_institute_staff()

    def perform_update(self, serializer):
        return usecase.CustomInstituteUpdate(
            instance=self.get_object(),
            serializer=serializer
        ).execute()

class UpdateInstituteStaffRoleView(generics.UpdateWithMessageAPIView,InstituteStaffMixins):
    serializer_class = serializers.UpdateInstituteStaffRoleSerializer
    def get_object(self):
        return self.get_institute_staff()

    def perform_update(self, serializer):
        return usecase.CustomInstituteUpdate(
            instance=self.get_object(),
            serializer=serializer
        ).execute()

class UpdateInstituteView(generics.UpdateWithMessageAPIView,InstituteMixins):
    """
    This endpoint is use to update institute
    """
    message = 'institute update successfully'
    serializer_class = serializers.UpdateInstituteSerializer
    

    def get_object(self):
        return self.get_institute()

    def perform_update(self, serializer):
        return usecase.UpdateInstituteUseCase(
            institute=self.get_object(),
            serializer = serializer
        ).execute()
#update logo
class UpdateInstituteLogoView(generics.UpdateWithMessageAPIView,InstituteMixins):
    """
    This endpoint is use to update institute logo
    """
    message = 'institute logo update successfully'
    serializer_class = serializers.UpdateInstituteLogoSerializer
    parser_classes = (MultiPartParser,FileUploadParser)
    def get_object(self):
        return self.get_institute()

    def perform_update(self, serializer):
        return usecase.UpdateInstituteUseCase(
            institute=self.get_object(),
            serializer = serializer
        ).execute()

#update coverimage
class UpdateInstituteCoverimageView(generics.UpdateWithMessageAPIView,InstituteMixins):
    """
    This endpoint is use to update institute coverimage
    """
    message = 'institute coverimage update successfully'
    serializer_class = serializers.UpdateInstituteCoverImageSerializer
    parser_classes = (MultiPartParser,FileUploadParser)

    def get_object(self):
        return self.get_institute()

    def perform_update(self, serializer):
        return usecase.UpdateInstituteUseCase(
            institute=self.get_object(),
            serializer = serializer
        ).execute()


class ListInstituteView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    serializer_class = serializers.ListInstituteSerializer
    filter_class = InstituteFilter
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['name','course_related__course__name','course_related__faculty__name']
    # https://www.django-rest-framework.org/api-guide/filtering/
    def get_queryset(self):

        return usecase.ListInstituteUseCase().execute()

class UpdateBrochureView(generics.UpdateWithMessageAPIView,InstituteMixins):
    """
    this endpoint is use to update institute broucher
    """
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    serializer_class = serializers.UpdateBrochureSerializer

    def get_object(self):
        # is_auth = CheckPermission(permissions=["ACTION_INSTITUTE_APPLICATION"], user=self.request.user).has_permission()
        return self.get_institute()

    def perform_update(self, serializer):
        return usecase.UpdateInstituteUseCase(
            institute=self.get_institute(),
            serializer=serializer,
        ).execute()

class DetailInstituteView(generics.RetrieveAPIView,Institute,InstituteMixins):
    """
    this endpoint is use to get institute detail
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.InstituteDetailSerilaizer

    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecase.GetInstituteDetailUseCase(
            institute_id=self.get_object()
        ).execute()

    def get_serializer_context(self):
        context = super(DetailInstituteView, self).get_serializer_context()
        context.update({"request": self.request})
        return context
 
class AddScholorshipView(generics.CreateWithMessageAPIView,InstituteMixins):
    """
    This endpoint is use to add scholorship
    """
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    serializer_class = serializers.AddScholorshipSerializer
    message = "Add scholorship successfully"
    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecase.AddScholorshipUseCase(
            institute = self.get_object(),
            serializer =serializer
        ).execute()


class GetScholorshipListView(generics.ListAPIView,InstituteMixins):
    """
    this endpoint is use to get scholorship
    """
    serializer_class = serializers.GetScholorshipSerializer
    permission_classes = (AllowAny,)
    no_content_error_message = _('No scholorship at this moment')
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecase.ListScholorshipUseCase(
            institute = self.get_object()
        ).execute()
        
class UpdateScholorshipView(generics.UpdateWithMessageAPIView,ScholorshipMixins):
    """
    This endpoint is use to update scholorship
    """
    serializer_class = serializers.AddScholorshipSerializer
    message =_("update successfullt")
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    def get_object(self):
        return self.get_scholorship()

    def perform_update(self, serializer):
        return usecase.UpdateScholorshipUseCase(
            scholorship=self.get_object(),
            serializer=serializer
        ).execute()
#  AddScholorshipSerializer
class DeleteScholorshipView(generics.DestroyWithMessageAPIView,ScholorshipMixins):
    """
    This endpoint is use to delete scholorship
    """
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    message =_("delete successfully")
    def get_object(self):
        return self.get_scholorship()

    def perform_destroy(self, instance):
        return usecase.DeleteScholorshipUseCase(
            scholorship=self.get_object()
        ).execute()


class AddSolicalMediaView(generics.CreateWithMessageAPIView,InstituteMixins):
    """
    this endpoint is use to add sociali media
    """
    message = _("social media added")
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    serializer_class = serializers.AddSocialMediaSerializer
    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecase.SocialiMedialinkUseCase(
            institute=self.get_object(),
            serializer=serializer
        ).execute()


class DeleteSocialMediaView(generics.DestroyWithMessageAPIView,SocialMediaMixins):
    """
    This endpont is use to delete social media
    """
    message = _("social media delete successfully")
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    def get_object(self):
        return self.get_socialmedia()

    def perform_destroy(self, instance):
        return usecase.DeleteSocialMediaUseCase(
            socialmedia= self.get_object()
        ).execute()

class GetSocialMediaListView(generics.ListAPIView,InstituteMixins):
    """
    This api is use to get social media link
    """
    serializer_class = serializers.GetSocialMediaSerializer

    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecase.GetSocialMediaLinkListUseCase(
            institute=self.get_object()
        ).execute()

class AddFacilityView(generics.CreateWithMessageAPIView,InstituteMixins):
    """
    This end point is use to add facility
    """
    serializer_class =serializers.AddInstituteFacilitySerializer
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecase.CreateInstituteFacilityUseCase(
            serializer=serializer,
            institute=self.get_object()
        ).execute()

class FacilityList(generics.ListAPIView):
    serializer_class = serializers.FacilityListSerializer

    def get_queryset(self):
        return Facility.objects.all()

class DeleteFacility(generics.DestroyWithMessageAPIView,FacilityMixin):
    """
    this endpoint is use to delete
    """
    def get_object(self):
        return self.get_facility()

    def perform_destroy(self, instance):
        usecase.DeleteFacilityUseCase(
            facility=self.get_object()
        ).execute()

class GetFacilityView(generics.ListAPIView,InstituteMixins):
    """
    this endpoint is use to get facility
    """
    serializer_class = serializers.FacilitySerializer

    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecase.GetFacilityUseCase(
            institute= self.get_object()
        ).execute()



# class Dashboard(generics.)
class InstituteDetailView(generics.RetrieveAPIView):#todo institute detail view
    pass

class VerifiedInstituteView(generics.UpdateWithMessageAPIView,InstituteMixins):
    serializer_class = serializers.VerifyInstituteSerializer

    def get_object(self):
        return self.get_institute()

    def perform_update(self, serializer):
        return usecase.CustomInstituteUpdate(
            instance=self.get_object(),
            serializer=serializer,
        ).execute()

class VerifyUserAndChangePassword(generics.CreateAPIView,InstituteStaffMixins):
    serializer_class = serializers.VerifyChangePasswordSerializer
    def get_object(self):
        return self.get_institute_staff().user

    def perform_create(self, serializer):
        return usecase.VerifyAndChangePasswordUseCase().execute()


