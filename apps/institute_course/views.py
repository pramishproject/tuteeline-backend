from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.consultancy.mixins import ConsultancyMixin
from apps.institute_course.filter import ApplicationFilter, ApplicationAggregateFilter, FilterInstituteCourse
from apps.institute_course.mixins import ApplyMixin, CourseMixin, FacultyMixin
from apps.institute.mixins import InstituteMixins

from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.core.cache import cache

from apps.core import generics
from apps.institute_course.models import InstituteApply
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
    ConsultancyActionSerializer, InstituteApplicationStatus, InstituteApplicationCountSerializer,
    InstituteCourseSerializer)

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
    # permission_classes = (AllowAny,)

    no_content_error_message = _("No institute  course at the moment.")
    queryset = ''

    filter_class = FilterInstituteCourse
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["course__name","faculty__name"]
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.GetInstituteCourseUseCase(
            inst=self.get_object()
        ).execute()

    def get_serializer_context(self):
        context = super(ListInstituteCourse, self).get_serializer_context()
        context.update({"request": self.request})
        cache.delete('application')
        return context


class CourseDetailView(generics.RetrieveAPIView,CourseMixin):
    serializer_class = InstituteCourseSerializer
    def get_object(self):
        return self.get_institutecourse()

    def get_queryset(self):
        return usecases.InstituteCourseDetailUseCase(
            course=self.get_object(),
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
    filter_class = ApplicationFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["institute__course_related__course__name", "student__fullname"]
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListStudentApplicationCourseUseCase(
            institute=self.get_object()
        ).execute()

class ListStudentApplicationForCounsultancy(generics.ListAPIView,ConsultancyMixin):
    serializer_class = GetStudentApplicationInstituteSerializer
    filter_class = ApplicationFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["institute__course_related__course__name", "student__fullname"]

    def get_object(self):
        return self.get_consultancy()

    def get_queryset(self):
        return usecases.ListStudentApplicationConsultancyCourseUseCase(
            consultancy=self.get_object()
        ).execute()


class CancelStudentApplication(generics.UpdateWithMessageAPIView,ApplyMixin):
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
    filter_class = ApplicationAggregateFilter
    filter_backends = [DjangoFilterBackend]
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ApplicationDashboardUsecase(
            institute=self.get_object()
        ).execute()

class CountApplicationStatus(generics.ListAPIView,InstituteMixins):
    """
    count student application
    """
    serializer_class = InstituteApplicationCountSerializer
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.CountApplicationUseCase(
            institute=self.get_object()
        ).execute()


class ListInstituteActionHistoryView(generics.ListAPIView,ApplyMixin):
    """
    action history list
    """
    serializer_class = InstituteApplicationStatus

    def get_object(self):
        return self.get_apply()

    def get_queryset(self):
        return usecases.ListInstituteActionHistoryUseCase(
            apply=self.get_object(),
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

import uuid
from rest_framework.response import Response
class DownloadStudentApplication(APIView):
    def get(self,request,application_id):
        # Create a file-like buffer to receive PDF data.

        application = uuid.UUID(application_id)
        self._application = InstituteApply.objects.get(id=application)
        data = GetMyApplicationDetailForInstituteSerializer(self._application,many=False).data
        student=data.pop('student')
        # address = data.pop("address_relation")
        course = data.pop('apply_to')
        identity = data.pop('checked_student_identity')
        essay =data.pop('checked_student_essay')
        sop = data.pop('checked_student_sop')
        academic = data.pop('checked_student_academic')
        lor = data.pop('checked_student_lor')
        institute = data.pop('institute')
        consultancy = data.pop('apply_from')
        action = data.pop('action')
        action_by = data.pop('action_field')
        consultancy =data.pop('consultancy')
        faculty =data.pop('faculty')
        print(data,dict(student),dict(identity))
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, "Tuteeline")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        file_name = application_id+".pdf"
        return FileResponse(buffer, as_attachment=True, filename=file_name)
        # return Response({"c":1})
