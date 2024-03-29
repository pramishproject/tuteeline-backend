
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.core import generics
from apps.institute.mixins import InstituteMixins
from rest_framework.response import Response
from apps.students import serilizers, usecases
from apps.students.mixins import AddressMixin, FavouriteMixin, StudentMixin
from apps.students.models import StudentModel


# Create your views here.
from apps.user.permissions import IsStudentUser


class RegisterStudentView(generics.CreateWithMessageAPIView):
    """
    use this endpoind to register institute
    """
    parser_classes = (MultiPartParser, FileUploadParser,)
    message = _('Registered successfully')
    permission_classes = (AllowAny,)
    serializer_class = serilizers.RegisterStudentSerializer

    def perform_create(self, serializer):

        return usecases.RegisterStudentUseCase(
            serializer=serializer
        ).execute()



class StudentInitProfileView(generics.RetrieveAPIView, StudentMixin):
    """
    Use this endpoint to get student detail
    """
    permission_classes = (IsAuthenticated,IsStudentUser)
    serializer_class = serilizers.StudentDetailSerializer
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        profile=usecases.GetStudentUserUseCase(
            student=self.get_object()
            ).execute()
        return profile




class UpdateStudentView(generics.UpdateWithMessageAPIView,StudentMixin):
    """
    use this endpoint to update student 
    """
    message = _("update student detail successfully")
    serializer_class = serilizers.UpdateStudentSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_update(self, serializer):
        return usecases.UpdateStudentUseCase(
            student=self.get_student(),
            serializer = serializer
        ).execute()

class UpdateImageView(generics.UpdateWithMessageAPIView,StudentMixin):
    """
    use this endpoint to update profile
    """
    message = _("update profile is success")
    serializer_class = serilizers.UpdateProfilePictureSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_update(self, serializer):
        return usecases.UpdateProfilePictureUseCase(
            student=self.get_student(),
            serializer = serializer
        ).execute()

class StudentAddressView(generics.CreateWithMessageAPIView,StudentMixin):
    """
    this end point is use to take student address
    """
    message =_("address complete successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)
    serializer_class = serilizers.StudentAddressSerializer

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.AddStudentAddressUseCase(
            student_id= self.get_object(),
            serializer = serializer
        ).execute()

class StudentAddressUpdateView(generics.UpdateWithMessageAPIView,AddressMixin):
    """
    This endpoint is use to update student address
    """
    message = _("address update successfully")
    permission_classes = (AllowAny,)
    serializer_class = serilizers.StudentAddressSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_address().student.user)
        return self.get_address()

    def perform_update(self, serializer):
        return usecases.StudentAddressUpdateUseCase(
            address= self.get_object(),
            serializer = serializer
        ).execute()


class GetStudentAddressView(generics.RetrieveAPIView,AddressMixin):
    """
    This endpoint is use to get student address
    """
    permission_classes = (IsAuthenticated, IsStudentUser)
    serializer_class = serilizers.StudentAddressSerializer
    def get_object(self):
        self.check_object_permissions(self.request, self.get_address().student.user)
        return self.get_address()
    def get_queryset(self):
        return usecases.GetStudentAddressUseCase(
            address=self.get_queryset()
        )

class StudentLatitudeAndLongitudeUpdate(generics.UpdateWithMessageAPIView,StudentMixin):
    """
    this endpoint is use to update latitude and longitude
    """
    permission_classes = (IsAuthenticated, IsStudentUser)
    serializer_class = serilizers.StudentLatitudeLongitudeUpdate

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_update(self, serializer):
        return usecases.StudentLatitudeLongitudeUpdateUseCase(
            student=self.get_object(),
            serializer = serializer
        ).execute()

class AddFavouriteInstitute(generics.CreateWithMessageAPIView,StudentMixin):
    """
    This endpoint is use to add bookmark
    """
    permission_classes = (IsAuthenticated, IsStudentUser)
    serializer_class = serilizers.AddFavouriteInstituteSerializer
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()
    def perform_create(self,serializer):
        return usecases.AddFavourateInstituteUseCase(
            serializer = serializer,
            student = self.get_object()
        ).execute()


class GetFavouriteInstitute(generics.ListAPIView,StudentMixin):
    """
    This endpoint is use to get fav student institute
    """
    permission_classes = (IsAuthenticated, IsStudentUser)
    serializer_class  = serilizers.GetFavouriteInstituteSerializer
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.GetFavouriteInstituteUseCase(
            student = self.get_object()
        ).execute()

class DeleteFavouriteInstitute(generics.DestroyWithMessageAPIView,FavouriteMixin):
    """
    this endpoint is use to delete favourite
    """
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_favourite().student.user)
        return self.get_favourite()

    def perform_destroy(self, instance):
        return usecases.DeleteFavouriteInstitute(
            favourite = self.get_object(),
        ).execute()

class CreateInstituteVisitorView(generics.CreateWithMessageAPIView,StudentMixin):
    """
    This endpoint is use to create visitor
    """
    serializer_class = serilizers.CreateInstituteVisiterSerializer
    message = _("institute visitor Create Successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateInstituteViewersUseCase(
            student=self.get_object(),
            serializer = serializer
        ).execute()

class ListVisitorHistryView(generics.ListAPIView,StudentMixin):
    """
    This endpoint is use to list histry
    """
    serializer_class = serilizers.ListVisitorHistrySerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.GetStudentHistryUseCase(
            student=self.get_object(),
        ).execute()

class DeActivateStudent(generics.UpdateWithMessageAPIView,StudentMixin): #todo
    """
    This endpoint is use to deactivate student
    """

class GetStudentDetailView(generics.RetrieveAPIView,StudentMixin):
    serializer_class = serilizers.GetStudentDetailSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.GetStudentDetailUseCase(
            student=self.get_object()
        ).execute()


class CountInstituteVisitors(APIView):
    def get(self,request,institute_id):
        count = usecases.CountInstituteVisitor(
            institute=institute_id
        ).execute()
        return Response(
            {
                "count":count
            },status=200
        )

# portal
class ListStudentsForPortal(generics.ListAPIView):
    serializer_class = serilizers.StudentDetailSerializer
    # permission_classes = (IsAuthenticated, IsStudentUser) #todo
    def get_queryset(self):
        return StudentModel.objects.all()