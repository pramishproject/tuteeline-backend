import json

from django.db.models import Count
from django.db.models.functions import TruncDay,TruncWeek,TruncMonth,TruncYear
from django.utils.datetime_safe import datetime
from datetime import  timedelta
import pandas as pd

from apps.academic.exceptions import AcademicNotFound, LorNotFound, SopNotFound, EssayNotFound
from apps.academic.models import Academic, PersonalEssay, StudentLor, StudentSop
from apps.consultancy.models import Consultancy
from apps.core.usecases import BaseUseCase
from apps.institute.models import Institute, InstituteStaff
from apps.institute_course.exceptions import CourseNotFound, FacultyNotFound, InstituteApplyNotFound, InstituteNotFound, \
    InstituteStaffNotFound, UniqueStudentApply, VoucherNotFound, CheckDocumentDoesntExist, DocTypeNotFound, \
    VoucherFileDoesntExist
from apps.institute_course.models import CommentApplicationInstitute, InstituteApply, InstituteCourse, Course, Faculty, \
    CheckedAcademicDocument, CheckStudentIdentity, CheckedStudentLor, CheckedStudentSop, CheckedStudentEssay, \
    ApplyAction, ActionApplyByConsultancy, VoucherFile
from apps.studentIdentity.exceptions import CitizenshipNotFound,PassportNotFound
from apps.studentIdentity.models import Citizenship, Passport
from apps.payment_method.models import Transaction
from apps.utils.uuid_validation import is_valid_uuid


WEEK_TIME="WEEK_TIME"
DAY_TIME = "DAY_TIME"
MONTH_TIME = "MONTH_TIME"
YEAR_TIME ="YEAR_TIME"


APPLY_DOC_TYPE_ACADEMIC="ACADEMIC"
APPLY_DOC_TYPE_LOR="LOR"
APPLY_DOC_TYPE_SOP="SOP"
APPLY_DOC_TYPE_ESSAY="ESSAY"
APPLY_DOC_TYPE_IDENTITY="IDENTITY"
APPLY_DOC_TYPE_CITIZENSHIP ="CITIZENSHIP"
APPLY_DOC_TYPE_PASSWORD ="PASSWORD"

class AddCourseUseCase(BaseUseCase):
    def __init__(self , serializer ,institute:Institute):
        self._institute= institute
        self._serializer=serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._course = InstituteCourse.objects.create(
            **self._serializer,
            institute=self._institute
            )
   


class GetInstituteCourseUseCase(BaseUseCase):
    def __init__(self,inst):
        self._institute = inst

    def execute(self):
        self._factory()
        return self._course

    def _factory(self):
        # self._course = InstituteCourse.objects.filter(institute=self._institute).prefetch_related('course','faculty').\
        #     select_related("")
        self._course = InstituteCourse.objects.filter(institute=self._institute).\
            select_related('course','faculty')

class InstituteCourseDetailUseCase(BaseUseCase):
    def __init__(self,course):
        self._institute_course = course

    def execute(self):
        self._factory()
        return self._course

    def _factory(self):
        # self._course = InstituteCourse.objects.filter(institute=self._institute).prefetch_related('course','faculty').\
        #     select_related("")
        self._course = InstituteCourse.objects.get(pk=self._institute_course).\
            select_related('course','faculty')

class GetCourseUseCase(BaseUseCase):
    def __init__(self,institute_course_id):
        self._course_id = institute_course_id

    def execute(self):
        self._factory()
        return self._course

    def _factory(self):
        try:
            self._course = InstituteCourse.objects.get(pk=self._course_id)
        except InstituteCourse.DoesNotExist:
            raise CourseNotFound


class UpdateInstituteCourseUseCase(BaseUseCase):
    def __init__(self,serializer,institute_course:InstituteCourse):
        self._institute_course =institute_course
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._institute_course,key,self._data.get(key))

        self._institute_course.updated_at = datetime.now()
        self._institute_course.save()


class DeleteInstituteCourseUseCase(BaseUseCase):
    def __init__(self,institute_course:InstituteCourse):
        self._institute_course = institute_course

    def execute(self):
        print(self._institute_course.institute)
        self._factory()

    def _factory(self):
        self._institute_course.delete()


class ListFacultyUseCase(BaseUseCase):
    def execute(self):
        return Faculty.objects.all()


class GetFacultyUseCase(BaseUseCase):
    def __init__(self,faculty_id):
        self._faculty_id = faculty_id

    def execute(self):
        self._factory()
        return self._faculty

    def _factory(self):
        try:
            self._faculty = Faculty.objects.get(pk = self._faculty_id)

        except Faculty.DoesNotExist:
            raise FacultyNotFound

class GetVoucherFileUseCase(BaseUseCase):
    def __init__(self,voucher_id):
        self._voucher_id=voucher_id

    def execute(self):
        self._factory()
        return self._voucher

    def _factory(self):
        try:
            self._voucher = VoucherFile.objects.get(pk=self._voucher_id)

        except VoucherFile.DoesNotExist:
            raise VoucherNotFound

class GetApplyDocumentUseCase(BaseUseCase):
    def __init__(self,apply_doc_id,doc_type):
        self._apply_doc_id = apply_doc_id
        self._doc_type = doc_type

    def execute(self):
        self._factory()
        print(self._doc)
        return self._doc

    def _factory(self):
        if self._doc_type == APPLY_DOC_TYPE_ACADEMIC:
            try:
                self._doc = CheckedAcademicDocument.objects.get(id=self._apply_doc_id)
            except CheckedAcademicDocument.DoesNotExist:
                raise CheckDocumentDoesntExist

        elif self._doc_type == APPLY_DOC_TYPE_ESSAY:
            try:
                self._doc = CheckedStudentEssay.objects.get(pk=self._apply_doc_id)
            except CheckedStudentEssay.DoesNotExist:
                raise CheckDocumentDoesntExist

        elif self._doc_type == APPLY_DOC_TYPE_LOR:
            try:
                self._doc = CheckedStudentLor.objects.get(pk=self._apply_doc_id)
            except CheckedStudentLor.DoesNotExist:
                raise CheckDocumentDoesntExist

        elif self._doc_type == APPLY_DOC_TYPE_SOP:
            try:
                self._doc = CheckedStudentSop.objects.get(pk=self._apply_doc_id)
            except CheckedStudentSop.DoesNotExist:
                raise CheckDocumentDoesntExist

        elif self._doc_type == APPLY_DOC_TYPE_IDENTITY:
            try:
                self._doc = CheckStudentIdentity.objects.get(pk=self._apply_doc_id)
            except CheckStudentIdentity.DoesNotExist:
                raise CheckDocumentDoesntExist
        else:
            raise DocTypeNotFound

class DeleteVoucherUseCase(BaseUseCase):
    def __init__(self,instance:VoucherFile):
        self._instance = instance

    def execute(self):
        self._factory()

    def _factory(self):
        self._instance.delete()

class ListCourseUseCase(BaseUseCase):
    def __init__(self,faculty):
        self._faculty = faculty

    def execute(self):
        self._course = Course.objects.filter(faculty = self._faculty)
        return self._course


class ApplyUseCase(BaseUseCase):
    def __init__(self,serializer):
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        academics = self._data.pop('academic')
        citizenship = self._data.pop("citizenship").strip()
        passport = self._data.pop("passport").strip()
        sop =  self._data.pop("sop").strip()
        lors = self._data.pop("lor")
        essay = self._data.pop("essay").strip()

        try:
            self._apply = InstituteApply.objects.create(
                **self._data
            )
            self.status = ApplyAction.objects.create(
                apply=self._apply,
            )
            self.consultancy_status = ActionApplyByConsultancy.objects.create(
                apply=self._apply
            )
            self._apply.action_field = self.status
            self._apply.consultancy_action = self.consultancy_status
            self._apply.save()

        except InstituteApply.validate_unique():
            raise UniqueStudentApply

        academic_list = []
        for academic in academics:
            try:
                academic_obj=Academic.objects.get(pk=academic)
                academic_list.append(CheckedAcademicDocument(
                    application=self._apply,
                    academic=academic_obj
                ))
            except Academic.DoesNotExist:
                raise AcademicNotFound


        if len(academic_list) > 0:
            CheckedAcademicDocument.objects.bulk_create(
                    academic_list
                )


        if len(citizenship)>0 or len(passport):

            identity=CheckStudentIdentity(
                application = self._apply,
            )
            ok1 = is_valid_uuid(citizenship)
            if ok1:
                try:
                    citizenship= Citizenship.objects.get(pk=citizenship)
                except Citizenship.DoesNotExist:
                    raise CitizenshipNotFound
                identity.citizenship = citizenship
            ok = is_valid_uuid(passport)
            if ok:
                try:
                    passport = Passport.objects.get(pk=passport)
                    identity.passport=passport
                except Passport.DoesNotExist:
                    raise PassportNotFound
            if ok1 or ok:
                identity.save()

        lor_list =[]
        for lor in lors:
            try:
                lor=StudentLor.objects.get(pk=lor)
                lor_list.append(
                    CheckedStudentLor(
                        application=self._apply,
                        lor = lor,
                    )
                )
            except StudentLor.DoesNotExist:
                raise LorNotFound

        if len(lor_list)>0:
            CheckedStudentLor.objects.bulk_create(lor_list)

        if len(sop) > 0:
            ok = is_valid_uuid(sop)
            if ok:
                try:
                    sop = StudentSop.objects.get(pk=sop)
                    sop_obj = CheckedStudentSop(
                        application=self._apply,
                        sop = sop
                    )
                    sop_obj.save()
                except StudentSop.DoesNotExist:
                    raise SopNotFound

        if len(essay) > 0:
            ok = is_valid_uuid(essay)
            if ok:
                try:
                    essay = PersonalEssay.objects.get(pk=essay)
                    CheckedStudentEssay.objects.create(
                        application=self._apply,
                        essay=essay
                    )
                except PersonalEssay.DoesNotExist:
                    raise EssayNotFound

class AddCheckDocumentUseCase(BaseUseCase):
    def __init__(self,doc_type,doc_id,apply):
        self._doc_id = doc_id
        self._doc_type =doc_type
        self._apply = apply

    def execute(self):
        self._factory()

    def _factory(self):
        if self._doc_type == APPLY_DOC_TYPE_CITIZENSHIP:
            try:
                citizenship = Citizenship.objects.get(pk=self._doc_id)
                identity = CheckStudentIdentity(
                    application=self._apply,
                    citizenship = citizenship,
                )
                identity.save()
            except Citizenship.DoesNotExist:
                raise CitizenshipNotFound

        elif self._doc_type == APPLY_DOC_TYPE_PASSWORD:
            try:
                passport = Passport.objects.get(pk=self._doc_id)
                identity = CheckStudentIdentity(
                    application=self._apply,
                    passport=passport,
                )
                identity.save()
            except Passport.DoesNotExist:
                raise PassportNotFound

        elif self._doc_type == APPLY_DOC_TYPE_SOP:
            try:
                sop = StudentSop.objects.get(pk=self._doc_id)
                sop_obj = CheckedStudentSop(
                    application=self._apply,
                    sop=sop
                )
                sop_obj.save()
            except StudentSop.DoesNotExist:
                raise SopNotFound

        elif self._doc_type == APPLY_DOC_TYPE_LOR:
            try:
                lor=StudentLor.objects.get(pk=self._doc_id)
                check_lor =  CheckedStudentLor(
                        application=self._apply,
                        lor = lor,
                    )
                check_lor.save()
            except StudentLor.DoesNotExist:
                raise LorNotFound

        elif self._doc_type == APPLY_DOC_TYPE_ESSAY:
            try:
                essay = PersonalEssay.objects.get(pk=self._doc_id)
                CheckedStudentEssay.objects.create(
                    application=self._apply,
                    essay=essay
                )
            except PersonalEssay.DoesNotExist:
                raise EssayNotFound

        elif self._doc_type == APPLY_DOC_TYPE_ACADEMIC:
            try:
                academic_obj = Academic.objects.get(pk=self._doc_type)
                academic=CheckedAcademicDocument(
                    application=self._apply,
                    academic=academic_obj
                )
                academic.save()
            except Academic.DoesNotExist:
                raise AcademicNotFound
        else:
            raise DocTypeNotFound
class InstituteActionUseCase(BaseUseCase):
    def __init__(self,apply,serializer):
        self._apply = apply
        self._serializer = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):

        self.status = ApplyAction.objects.create(
            **self._serializer,
            apply=self._apply
            )
        self._apply.action_field = self.status
        self._apply.action = self.status.action
        self._apply.updated_at = datetime.now()
        self._apply.save()

class ConsultancyActionUseCase(BaseUseCase):
    def __init__(self,apply,serializer):
        self._apply = apply
        self._serializer = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self.consultancy_status = ActionApplyByConsultancy.objects.create(
            **self._serializer,
            apply=self._apply,
        )
        self._apply.consultancy_action = self.consultancy_status
        self._apply.updated_at = datetime.now()
        self._apply.save()

class RequestForApplicationFeeUseCase(BaseUseCase):
    def __init__(self,apply:InstituteApply,serializer):
        self._apply = apply
        self._serializer = serializer
        self._data = self._serializer.validated_data
    def execute(self):
        self._factory()

    def _factory(self):
        staff_id = self._data.pop("staff_id")
        try:
            staff = InstituteStaff.objects.get(pk=staff_id)
            apply_action=ApplyAction.objects.create(
                apply=self._apply,
                institute_user = staff,
                action="payment_requested"
            )
            self._apply.request_for_application_fee = True
            self._apply.action = "payment_requested"
            self._apply.action_field =apply_action
            self._apply.updated_at = datetime.now()

            self._apply.save()
        except InstituteStaff.DoesNotExist:
            raise InstituteStaffNotFound


class ApproveApplicationVoucher(BaseUseCase):
    def __init__(self,apply:InstituteApply,serializer):
        self._apply = apply
        self._serializer = serializer
        self._data = self._serializer.validated_data
    def execute(self):
        self._factory()

    def _factory(self):
        staff_id = self._data.pop('approve_by')
        voucher_id = self._data.pop("voucher_id")
        voucher = None
        if voucher_id != None or len(voucher_id) >0:
            try:
                voucher = VoucherFile.objects.get(pk=voucher_id)

            except VoucherFile.DoesNotExist:
                raise VoucherFileDoesntExist
        try:

            staff = InstituteStaff.objects.get(pk=staff_id)
            self._apply.approve_application_fee = staff

            dictionary = {
                "apply_id": str(self._apply.id)
            }
            json_object = json.dumps(dictionary, indent=4)
            payment_type = self._data.pop('payment_type')
            payment_method = self._data.pop('payment_method')

            Transaction.objects.create(
                institute=self._apply.institute,
                payment_type=payment_type,
                payment_method=payment_method,
                amount=self._apply.course.reg_fee,
                student=self._apply.student,
                json_data=json_object,
            )
            user_action = ApplyAction.objects.create(
                apply=self._apply,
                institute_user = staff,
                action= 'payment_verify',
            )
            self._apply.action = "payment_verify"
            self._apply.action_field = user_action
            self._apply.updated_at = datetime.now()
            self._apply.save()
            if voucher:
                voucher.approve=True
                voucher.updated_at = datetime.now()
                voucher.save()
        except InstituteStaff.DoesNotExist:
            raise InstituteStaffNotFound


class ListStudentMyApplication(BaseUseCase):
    def __init__(self,student):
        self._student = student

    def execute(self):
        self._factory()
        return self._application

    def _factory(self):
        self._application = InstituteApply.objects.filter(student=self._student)

class ListPaymentVoucherUseCase(BaseUseCase):
    def __init__(self,apply):
        self._apply =  apply

    def execute(self):
        self._factory()
        return self._voucher

    def _factory(self):
        self._voucher = VoucherFile.objects.filter(apply=self._apply)

class GetMyApplicationDetailUsecase(BaseUseCase):
    def __init__(self,application):
        self._application = application

    def execute(self):
        self._factory()
        return self._application_detail

    def _factory(self):
        self._application_detail = InstituteApply.objects.get(pk= self._application).prefetch_related("course").prefetch_related(
            "checked_student_academic"
        ).prefetch_related(
            "checked_student_lor"
        ).prefetch_related(
            "checked_student_identity"
        ).prefetch_related(
            "checked_student_sop"
        ).prefetch_related(
            "checked_student_essay"
        )

class GetApplicationDetailForInstituteUsecase(BaseUseCase):
    def __init__(self,application):
        self._application = application

    def execute(self):
        self._factory()
        return self._application_detail

    def _factory(self):
        self._application_detail = InstituteApply.objects.get(pk= self._application).prefetch_related("student").prefetch_related(
            "checked_student_academic"
        ).prefetch_related(
            "checked_student_lor"
        ).prefetch_related(
            "checked_student_identity"
        ).prefetch_related(
            "checked_student_sop"
        ).prefetch_related(
            "checked_student_essay"
        )
            # .prefetch_related(
        #     "student__address_relation"
        # )
class ListStudentApplicationCourseUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._apply

    def _factory(self):
        self._apply = InstituteApply.objects.filter(institute=self._institute).distinct()

class ListStudentApplicationAssignInstituteStaffCourseUseCase(BaseUseCase):
    def __init__(self,staff):
        self._staff = staff

    def execute(self):
        self._factory()
        return self._apply

    def _factory(self):
        self._apply = InstituteApply.objects.filter(institute_staff_assign=self._staff).distinct()


class ListStudentApplicationConsultancyCourseUseCase(BaseUseCase):
    def __init__(self, consultancy):
        self._consultancy = consultancy

    def execute(self):
        self._factory()
        return self._apply

    def _factory(self):
        self._apply = InstituteApply.objects.filter(consultancy=self._consultancy).distinct()


class GetApplyInstitute(BaseUseCase):
    def __init__(self,apply_id):
        self._apply_id =apply_id

    def execute(self):
        self._factory()
        return self._apply

    def _factory(self):
        try:
            self._apply = InstituteApply.objects.get(pk = self._apply_id)

        except InstituteApply.DoesNotExist:
            raise InstituteApplyNotFound

class CancleStudentApplicationUseCase(BaseUseCase):
    def __init__(self,application:InstituteApply,serializer):
        self._application = application
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._application,key,self._data.get(key))

        self._application.updated_at = datetime.now()
        self._application.save()

class AddCommentApplyInstitute(BaseUseCase):
    def __init__(self,serializer,apply):
        self._apply = apply
        self._serializer = serializer

    def execute(self):
        self._factory()

    def _factory(self):
        try:
            institutestaff=InstituteStaff.objects.get(pk = str(self._serializer.data.pop('institute_user')[0]))
        
        except InstituteStaff.DoesNotExist:
            raise InstituteStaffNotFound

        CommentApplicationInstitute.objects.create(
            application = self._apply,
            institute_user = institutestaff,
            comment = self._serializer.data.pop('comment')
        )

class ListCommentInstituteUseCase(BaseUseCase):
    def __init__(self,apply):
        self._apply = apply

    def execute(self):
        self._factory()
        return self._comment

    def _factory(self):
        self._comment=CommentApplicationInstitute.objects.filter(
            application = self._apply
        )


class ApplicationDashboardUsecase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self.applicant

    def _factory(self):
        self.applicant=InstituteApply.objects.filter(
            institute=self._institute,
            ).annotate(date=TruncDay('created_at')).values("date","action").\
            annotate(action_count=Count('action'))

class CountApplicationUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._count

    def _factory(self):
        self._count = InstituteApply.objects.filter(
            institute=self._institute
        ).values("action").annotate(action_count=Count('action'))


class CompareInstituteCourseUseCase(BaseUseCase):
    def __init__(self,course):
        self._course = course

    def execute(self):
        self._factory()
        return self._institute_course

    def _factory(self):
        self._institute_course = InstituteCourse.objects.filter(pk=self._course).prefetch_related("institute")


class ListInstituteActionHistoryUseCase(BaseUseCase):
    def __init__(self,apply):
        self._apply = apply

    def execute(self):
        self._factory()
        return self._history
    def _factory(self):
        self._history = ApplyAction.objects.filter(apply = self._apply)

class AddVoucherFileUseCase(BaseUseCase):
    def __init__(self,application,serializer):
        self._application = application
        self._serializer = serializer.validated_data
        self._data = self._serializer

    def execute(self):
        self._factory()

    def _factory(self):
        VoucherFile.objects.create(
            apply=self._application,
            **self._data
        )


class GetChartUseCase(BaseUseCase):
    def __init__(self,institute,from_date:datetime,to_date:datetime,days:int):
        self._institute = institute
        self._from_date = from_date
        self._to_date = to_date
        self._day = days

    def execute(self):
        self._factory()
        return self.chart_data

    def _factory(self):
        self.chart_data = []
        self._data = InstituteApply.objects.filter(
            institute=self._institute,
            created_at__range=[self._from_date, self._to_date]
        )
        print(self._data)
        self._count = 0
        if self._day<= 7:
            self._count =  self._data.annotate(date=TruncDay('created_at')).values("date","action").\
                annotate(action_count=Count('action'))

            self._daysChart(DAY_TIME)
        elif self._day>7 and self._day < 35:
            self._count=self._data.annotate(date=TruncWeek('created_at')).values("date","action").\
                annotate(action_count=Count('action'))
            self._daysChart(WEEK_TIME)

        elif self._day > 35 and self._day < 365:
            self._count = self._data.annotate(date=TruncMonth('created_at')).values("date", "action"). \
                annotate(action_count=Count('action'))
            self._daysChart(MONTH_TIME)
        else:
            self._count = self._data.annotate(date=TruncYear('created_at')).values("date", "action"). \
                annotate(action_count=Count('action'))
            self._daysChart(YEAR_TIME)

    def _daysChart(self,time_type):
        label_count = 1
        print(self._count)
        while self._from_date < self._to_date:
            label = self._from_date
            # if time_type==DAY_TIME:
            date_from = self._from_date + timedelta(days=1)
            if time_type == WEEK_TIME:
                date_from = self._from_date + timedelta(weeks=1)
                label = "weak" + str(label_count)
                label_count = label_count +1

            elif time_type == MONTH_TIME:
                date_from = self._from_date + pd.DateOffset(months=1)
                label = self._from_date.month

            elif time_type == YEAR_TIME:
                date_from = self._from_date + pd.DateOffset(months=12)
                label = self._from_date.year

            applied = 0
            verify = 0
            accept = 0
            reject = 0
            hold = 0
            print(date_from)
            for application in self._count:
                applicationTimestamp=application['date'].replace(tzinfo=None)
                start = datetime(self._from_date.year, self._from_date.month, self._from_date.day)
                end   =  datetime(date_from.year,date_from.month, date_from.day)

                if applicationTimestamp>=start and applicationTimestamp < end:
                    if application['action']=="verify":
                        verify = application['action_count']+ verify
                    elif application['action'] == 'applied':
                        applied = application['action_count']+applied

                    elif application['action'] == 'accept':
                        accept = application['action_count']+accept

                    elif application['action'] == 'reject':
                        reject = application['action_count']+reject

                    elif application['hold'] == 'hold':
                        hold = application['action_count']+hold

            self.chart_data.append({
                "accept":accept,
                "reject":reject,
                "applied":applied,
                "hold": hold,
                "verify":verify,
                "label":label,
            })


            self._from_date = date_from


class DeleteCheckDocumentUseCase(BaseUseCase):
    def __init__(self,instance):
        self._instance = instance

    def execute(self):
        self._instance.delete()

