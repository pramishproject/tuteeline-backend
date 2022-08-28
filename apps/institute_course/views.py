from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.consultancy.mixins import ConsultancyMixin
from apps.institute_course.filter import ApplicationFilter, ApplicationAggregateFilter, FilterInstituteCourse
from apps.institute_course.mixins import ApplyMixin, CourseMixin, FacultyMixin, VoucherFileMixin, ApplyDocMixin
from apps.institute.mixins import InstituteMixins, InstituteStaffMixins

from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.institute_course.utils import parse_date
from apps.payment_method.serializers import TransactionSerializer
from apps.user.permissions import IsInstituteUser
from apps.utils.currency import RealTimeCurrencyConverter

from django.core.cache import cache

from rest_framework.response import Response
from django.http import HttpResponse

from apps.institute_course.utils import html_to_pdf
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
    InstituteCourseSerializer, AssignStudentApplicationToInstituteStaff, ApproveApplicationFeeSerializer,
    AddVoucherFileSerializer)

from apps.institute_course import usecases

from apps.students.mixins import StudentMixin


class AddInstituteCourse(generics.CreateWithMessageAPIView,InstituteMixins):
    """
    Use this endpoint to add course
    """
    message = _('Create successfully')
    serializer_class = AddInstituteCourseSerializer
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    
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
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    serializer_class = AddInstituteCourseSerializer
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
    # permission_classes = (IsAuthenticated, IsInstituteUser)
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
    # permission_classes = (IsAuthenticated, IsInstituteUser)

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
    # permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated, IsInstituteUser)
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
class RequestForApplicationFeeView(generics.UpdateWithMessageAPIView,ApplyMixin):
    serializer_class = ApproveApplicationFeeSerializer
    def get_object(self):
        return self.get_apply()

    def perform_update(self, serializer):
        return usecases.RequestForApplicationFeeUseCase(
            apply=self.get_object()
        ).execute()

class AddVoucherFile(generics.CreateWithMessageAPIView,ApplyMixin):
    serializer_class = AddVoucherFileSerializer

    def get_object(self):
        return self.get_apply()

    def perform_create(self, serializer):
        return usecases.AddVoucherFileUseCase(
            application=self.get_object(),
            serializer=serializer,
        ).execute()

class DeleteVoucherFile(generics.DestroyWithMessageAPIView,VoucherFileMixin):
    message = _("Delete Successfully")
    def get_object(self):
        return self.get_voucher()

    def perform_destroy(self, instance):
        return usecases.DeleteVoucherUseCase(
            instance=self.get_object()
        ).execute()


class ApproveApplicationVoucher(generics.CreateWithMessageAPIView,ApplyMixin):
    serializer_class = TransactionSerializer
    def get_object(self):
        return self.get_apply()

    def perform_create(self, serializer):
        return usecases.ApproveApplicationVoucher(
            apply=self.get_object(),
            serializer =serializer,
        ).execute()

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

class DeleteCheckDocument(generics.DestroyWithMessageAPIView,ApplyDocMixin):
    """
        APPLY_DOC_TYPE_ACADEMIC="ACADEMIC"
        APPLY_DOC_TYPE_LOR="LOR"
        APPLY_DOC_TYPE_SOP="SOP"
        APPLY_DOC_TYPE_ESSAY="ESSAY"
        APPLY_DOC_TYPE_IDENTITY="IDENTITY"
    """
    def get_object(self):
        return self.get_document()

    def perform_destroy(self, instance):
        return usecases.DeleteCheckDocumentUseCase(
            instance=self.get_object(),
        ).execute()

class AddCheckDocument(APIView,ApplyMixin):
    """
        APPLY_DOC_TYPE_ACADEMIC="ACADEMIC"
         APPLY_DOC_TYPE_LOR="LOR"
        APPLY_DOC_TYPE_SOP="SOP"
        APPLY_DOC_TYPE_ESSAY="ESSAY"
        APPLY_DOC_TYPE_IDENTITY="IDENTITY"
        APPLY_DOC_TYPE_CITIZENSHIP ="CITIZENSHIP"
        APPLY_DOC_TYPE_PASSWORD ="PASSWORD"
            """
    def post(self,request,doc_type,apply_doc_id,apply_id):
        # mixin = ApplyMixin()
        apply = self.get_apply()
        usecases.AddCheckDocumentUseCase(
            apply=apply,
            doc_type=doc_type,
            doc_id=apply_doc_id
        ).execute()
        return Response({"message":"Added successfully"},status=200)

class ListStudentApplicationView(generics.ListAPIView,InstituteMixins):
    """
    this api is use to list application
    """
    serializer_class = GetStudentApplicationInstituteSerializer
    filter_class = ApplicationFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["institute__course_related__course__name", "student__fullname"]
    permission_classes = (IsAuthenticated, IsInstituteUser)
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListStudentApplicationCourseUseCase(
            institute=self.get_object()
        ).execute()

class AssignInstituteStaffApplicationView(generics.ListAPIView,InstituteStaffMixins):
    serializer_class = GetStudentApplicationInstituteSerializer
    filter_class = ApplicationFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["institute__course_related__course__name", "student__fullname"]
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    def get_object(self):
        return self.get_institute_staff()

    def get_queryset(self):
        return usecases.ListStudentApplicationAssignInstituteStaffCourseUseCase(
            staff=self.get_object()
        ).execute()
class AssignApplicationToInstituteStaff(generics.UpdateWithMessageAPIView,ApplyMixin):
    serializer_class = AssignStudentApplicationToInstituteStaff
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    def get_object(self):
        return self.get_apply()

    def perform_update(self, serializer):
        return usecases.CancleStudentApplicationUseCase(
            application=self.get_object(),
            serializer = serializer
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
    # permission_classes = (IsAuthenticated, IsInstituteUser)
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
    # permission_classes = (IsAuthenticated, IsInstituteUser)
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
    # permission_classes = (IsAuthenticated, IsInstituteUser)
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



class DownloadStudentApplication(APIView):
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    def get(self,request,application_id):
        self._application = InstituteApply.objects.get(id=application_id)

        data = GetMyApplicationDetailForInstituteSerializer(self._application, many=False).data
        student = data.pop('student')
        address = data.pop("address")
        # course = data.pop('apply_to')
        # identity = data.pop('checked_student_identity')
        # essay = data.pop('checked_student_essay')
        # sop = data.pop('checked_student_sop')
        # academic = data.pop('checked_student_academic')
        # lor = data.pop('checked_student_lor')
        # institute_logo = self._application.institute.logo.url
        # apply_from = data.pop('apply_from')
        # action = data.pop('action')
        # action_by = data.pop('action_field')
        # consultancy =data.pop('consultancy')
        # faculty =data.pop('faculty')
        pdf = html_to_pdf('pdf/application.html', {"student":student,"address":address,
                                                   # "course":course,
                                                   # "identity":identity,"essay":essay,"sop":sop,
                                                   # "academic":academic,"lor":lor,"institute_logo":institute_logo,
                                                   # "consultancy":consultancy,"action":action,"apply_from":apply_from,
                                                   # "action_by":action_by,"faculty":faculty
                                                   })

        download = 'application/html'
        return HttpResponse(pdf, content_type=download)


import csv
from django.http import HttpResponse

class ApplicationCsv(APIView):
    def get(self,request):
        # Create the HttpResponse object with the appropriate CSV header.
        download = 'text/csv'
        view_csv = 'text/html'
        response = HttpResponse(
            content_type=view_csv,
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

        return response

class GetCurrency(APIView):
    def get(self,request):
        converter = RealTimeCurrencyConverter()
        return Response(dict(converter.CurrencyName()))


class InstituteChart(APIView):
    # permission_classes = (IsAuthenticated, IsInstituteUser)
    def get(self,request,institute_id,date_to,date_from):
        date_to = parse_date(date_to)
        date_from = parse_date(date_from)
        if date_to == None or date_from == None:
            return Response({"error":"data to and date from is not in format"},status=404)

        if date_to < date_from:
            return Response({"error":"date to is less then date from"})
        delta = date_to - date_from

        data = usecases.GetChartUseCase(
            institute=institute_id,
            from_date=date_from,
            to_date=date_to,
            days=int(delta.days),
        ).execute()
        return Response({"results":data})

