
from django.db import connection
from django.db.models import Count
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.academic.exceptions import AcademicNotFound, LorNotFound, SopNotFound, EssayNotFound
from apps.academic.models import Academic, PersonalEssay, StudentLor, StudentSop
from apps.consultancy.models import Consultancy
from apps.core.usecases import BaseUseCase
from apps.institute.models import Institute, InstituteStaff
from apps.institute_course.exceptions import CourseNotFound, FacultyNotFound, InstituteApplyNotFound, InstituteNotFound, \
    InstituteStaffNotFound, UniqueStudentApply
from apps.institute_course.models import CommentApplicationInstitute, InstituteApply, InstituteCourse, Course, Faculty, \
    CheckedAcademicDocument, CheckStudentIdentity, CheckedStudentLor, CheckedStudentSop, CheckedStudentEssay, \
    ApplyAction, ActionApplyByConsultancy
from apps.studentIdentity.exceptions import CitizenshipNotFound,PassportNotFound
from apps.studentIdentity.models import Citizenship, Passport
from apps.students.exceptions import StudentModelNotFound
from apps.students.models import StudentModel
from apps.utils.uuid_validation import is_valid_uuid


class AddCourseUseCase(BaseUseCase):
    def __init__(self , serializer ,institute:str):
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
        self._course = InstituteCourse.objects.filter(institute=self._institute).prefetch_related('course','faculty')
    


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
    def __init__(self,institute_course):
        self._institute_course = institute_course

    def execute(self):
        self._institute_course.delete()

class ListFacultyUseCase(BaseUseCase):
    def execute(self):
        return Faculty.objects.all()


class GetFacultyUseCase(BaseUseCase):
    def __init__(self,faculty_id):
        self._faculty = faculty_id

    def execute(self):
        return self._faculty

    def _factory(self):
        try:
            self._faculty = Faculty.objects.filter(pk = self._factory)

        except Faculty.DoesNotExist:
            raise FacultyNotFound


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
        self._apply.save()



class ListStudentMyApplication(BaseUseCase):
    def __init__(self,student):
        self._student = student

    def execute(self):
        self._factory()
        return self._application

    def _factory(self):
        self._application = InstituteApply.objects.filter(student=self._student)

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


class ListStudentApplicationCourseUseCase(BaseUseCase):
    def __init__(self, consultancy):
        self._consultancy = consultancy

    def execute(self):
        self._factory()
        return self._apply

    def _factory(self):
        self._apply = InstituteApply.objects.filter(consultancy=self._consultancy).distinct()


class GetApplyInstitute(BaseUseCase):
    def __init__(self,apply_id):
        self.apply_id =apply_id

    def execute(self):
        self._factory()
        return self._apply

    def _factory(self):
        try:
            self._apply = InstituteApply.objects.get(pk = "368a2abe-e56e-4793-b43a-c679d32cfbf7")

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
        # self._application.cancel = self._data.pop("cancel")
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
            # created_at__range=["2021-12-01", "2022-01-31"]
            ).values('action').annotate(Count('action'))




class CompareInstituteCourseUseCase(BaseUseCase):
    def __init__(self,course):
        self._course = course

    def execute(self):
        self._factory()
        return self._institute_course

    def _factory(self):
        self._institute_course = InstituteCourse.objects.filter(pk=self._course).prefetch_related("institute")





