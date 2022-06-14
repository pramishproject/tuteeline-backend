from apps.consultancy.mixins import ConsultancyMixin
from apps.institute_course.mixins import ApplyMixin, CourseMixin, FacultyMixin
from apps.institute.mixins import InstituteMixins

from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny


from apps.core import generics
from apps.institute_course.serializers import (
    ApplicationSerializerDashboard,
    CancelStudentApplicationSerializer,
    CommentApplicationSerializer,
    CourseSerializer,
    FacultySerializer,
    GetStudentApplicationInstituteSerializer,
    AddInstituteCourseSerializer,
    ListApplicationCommentSerializer,
    ListInstituteCourseSerializer,
    StudentApplySerializer, CompareInstituteSerializer, StudentMyApplicationListSerializer,
    GetMyApplicationDocumentSerializer, GetMyApplicationDetailForInstituteSerializer, InstituteActionSerializer,
    ConsultancyActionSerializer)

from apps.institute_course import usecases
# from apps.institute_course.mixins import InstituteCourseMixin
from apps.students.mixins import StudentMixin


class AddInstituteCourse(generics.CreateWithMessageAPIView,InstituteMixins):
    """
    Use this endpoint to add course
    """
    message = _('Create successfully')
    serializer_class = AddInstituteCourseSerializer
    permission_classes = (AllowAny,)
    
    def get_object(self):
        return self.get_institute()
    def perform_create(self, serializer):
        return usecases.AddCourseUseCase(
            serializer = serializer,
            institute = self.get_object()
             ).execute()

class ListInstituteCourse(generics.ListAPIView,InstituteMixins):
    """
    this end point is use to list course 
    put institute id in institute_id field
    """
    serializer_class = ListInstituteCourseSerializer
    permission_classes = (AllowAny,)
    no_content_error_message = _("No Consultancy staff at the moment.")
    queryset = ''
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.GetInstituteCourseUseCase(
            inst=self.get_object()
        ).execute()




class UpdateInstituteCourse(generics.UpdateWithMessageAPIView,CourseMixin):
    """
    This endpoint is use to update institute course
    """

    serializer_class = AddInstituteCourseSerializer
    permission_classes = (AllowAny,)
    message = _("update successfully")

    def get_object(self):
        return self.get_institutecourse()

    def perform_update(self, serializer):
        return usecases.UpdateInstituteCourseUseCase(
            institute_course=self.get_object(),
            serializer = serializer
        ).execute()



class DeleteInstituteCourseView(generics.DestroyWithMessageAPIView,CourseMixin):
    """
    This endpoint is use to destroy institute course
    """
    message = _("institute course delete successfully")

    def get_object(self):
        return self.get_institutecourse()

    def perform_destroy(self, instance):
        return usecases.DeleteInstituteCourseUseCase(
            institute_course= self.get_object()
        ).execute()


class ListFacultyView(generics.ListAPIView):
    """
    This endpoint is use to list faculty
    """
    serializer_class = FacultySerializer

    def get_queryset(self):
        return usecases.ListFacultyUseCase().execute()

class ListCourseView(generics.ListAPIView,FacultyMixin):
    """
    This end point is use to get course
    """
    serializer_class = CourseSerializer

    def get_object(self):
        return self.get_faculty()

    def get_queryset(self):
        return usecases.ListCourseUseCase(
            faculty= self.get_object()
        ).execute()



# application -----------------------------------------------------------------------------------------
class ListMyStudentApplication(generics.ListAPIView,StudentMixin):
    """
    list application
    """
    serializer_class = StudentMyApplicationListSerializer

    def get_queryset(self):
        return usecases.ListStudentMyApplication(
            student=self.get_student()
        ).execute()


class GetMyApplicationDetailView(generics.RetrieveAPIView,ApplyMixin):
    serializer_class = GetMyApplicationDocumentSerializer

    def get_object(self):
        return self.get_apply()
    def get_queryset(self):
        return usecases.GetMyApplicationDetailUsecase(
            application=self.get_object()
        ).execute()

class GetStudentApplicationDetailForInstitute(generics.RetrieveAPIView,ApplyMixin):
    serializer_class = GetMyApplicationDetailForInstituteSerializer

    def get_object(self):
        return self.get_apply()

    def get_queryset(self):
        return usecases.GetApplicationDetailForInstituteUsecase(
            application=self.get_object()
        ).execute()

class ApplyInstituteCourseView(generics.CreateAPIView):
    """
    This endpoint is use to apply
    """
    serializer_class = StudentApplySerializer
    message = _("student apply successfully")
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):

        return usecases.ApplyUseCase(
            serializer = serializer
        ).execute()

class ActionByInstitute(generics.CreateWithMessageAPIView,ApplyMixin):
    """
    this endpoint is use to
    """
    serializer_class = InstituteActionSerializer
    message =_("action successfully")
    def get_object(self):
        return self.get_apply()
    def perform_create(self, serializer):
        return usecases.InstituteActionUseCase(
            serializer=serializer,
            apply=self.get_object()
        ).execute()

class ActionByConsultancy(generics.CreateWithMessageAPIView,ApplyMixin):
    """
    This endpoint is use to action by consultancy user
    """
    serializer_class = ConsultancyActionSerializer
    message = _("action create successfullly")

    def get_object(self):
        return self.get_apply()

    def perform_create(self, serializer):
        return usecases.ConsultancyActionUseCase(
            apply=self.get_object(),
            serializer=serializer,
        ).execute()

class AddCommentApplicationView(generics.CreateWithMessageAPIView,ApplyMixin):
    """
    This api is use to comment on student application
    """
    serializer_class = CommentApplicationSerializer
    message = "comment successfully"

    def get_object(self):
        return self.get_apply()

    def perform_create(self, serializer):
        return usecases.AddCommentApplyInstitute(
            serializer =serializer,
            apply = self.get_object()
        )

class GetListCommentApplicationView(generics.ListAPIView,ApplyMixin):
    """
    this endpoint is use to get comment
    """
    serializer_class = ListApplicationCommentSerializer

    def get_object(self):
        return self.get_apply()

    def get_queryset(self):
        return usecases.ListCommentInstituteUseCase(
            apply = self.get_object()
        ).execute()

class ListStudentApplicationView(generics.ListAPIView,InstituteMixins):
    """
    this api is use to list application
    """
    serializer_class = GetStudentApplicationInstituteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["institute__course_related__course__name","student__fullname"]
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListStudentApplicationCourseUseCase(
            institute=self.get_object()
        ).execute()

class ListStudentApplicationForCounsultancy(generics.ListAPIView,ConsultancyMixin):
    serializer_class = GetStudentApplicationInstituteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["institute__course_related__course__name", "student__fullname"]

    def get_object(self):
        return self.get_consultancy()

    def get_queryset(self):
        return usecases.ListStudentApplicationCourseUseCase(
            consultancy=self.get_object()
        ).execute()


class CancleStudentApplication(generics.UpdateWithMessageAPIView,ApplyMixin):
    """
    This endpoint is used to cancel application
    """
    serializer_class = CancelStudentApplicationSerializer
    def get_object(self):
        return self.get_apply()

    def perform_update(self, serializer):
        return usecases.CancleStudentApplicationUseCase(
            application=self.get_object(),
            serializer = serializer
        ).execute()



class ApplicantDashboard(generics.ListAPIView,InstituteMixins):
    """
    student applicant dashboard
    """
    serializer_class = ApplicationSerializerDashboard
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ApplicationDashboardUsecase(
            institute=self.get_object()
        ).execute()



# -------------------------------------Application end-----------------------------


class CompareInstituteView(generics.RetrieveAPIView,CourseMixin): #TODO SPRINT1
    """
    Api For compare institute
    """
    serializer_class = CompareInstituteSerializer
    def get_object(self):
        return self.get_institutecourse()

    def get_queryset(self):
        return usecases.CompareInstituteCourseUseCase(
            course=self.get_object(),
        ).execute()


