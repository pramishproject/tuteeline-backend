
from django.db import connection
from django.db.models import Count
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from apps.academic.models import Academic, PersonalEssay, StudentLor, StudentSop
from apps.consultancy.models import Consultancy
from apps.core.usecases import BaseUseCase
from apps.institute.models import Institute, InstituteStaff
from apps.institute_course.exceptions import CourseNotFound, FacultyNotFound, InstituteApplyNotFound, InstituteNotFound, \
    InstituteStaffNotFound
from apps.institute_course.models import AccessOfAcademicDocument, AccessStudentEssay, AccessStudentIdentity, \
    AccessStudentLor, AccessStudentSop, CommentApplicationInstitute, InstituteApply, InstituteCourse, Course, Faculty
from apps.studentIdentity.models import Citizenship, Passport
from apps.students.exceptions import StudentModelNotFound
from apps.students.models import StudentModel
from apps.utils.dict_converter import QueryDataSerializer


class AddCourseUseCase(BaseUseCase):

    def __init__(self , serializer ,institute:str):
        self._institute= institute
        self._serializer=serializer

    def execute(self):
        self._factory()

    def _factory(self):
        try:
            course=Course.objects.get(pk=self._serializer.data.pop('course'))
        except Course.DoesNotExist:
            raise CourseNotFound

        try:
            faculty=Faculty.objects.get(pk=self._serializer.data.pop('faculty'))

        except Faculty.DoesNotExist:
            raise FacultyNotFound
        
        self._course = InstituteCourse.objects.create(
            program=self._serializer.data.pop('program'),
            faculty = faculty,
            course = course,
            intake = self._serializer.data.pop('intake'),
            eligibility = self._serializer.data.pop('eligibility'),
            score = self._serializer.data.pop('score'),
            last_mini_academic_score = self._serializer.data.pop('last_mini_academic_score'),
            duration_year = self._serializer.data.pop('duration_year'),
            total_fee = self._serializer.data.pop('total_fee'),
            fee_currency = self._serializer.data.pop('fee_currency'),
            reg_status = self._serializer.data.pop('reg_status'),
            reg_open = self._serializer.data.pop('reg_open'),
            reg_close = self._serializer.data.pop('reg_close'),
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
        self._serializer = serializer

    def execute(self):
        self._factory()

    def _factory(self):
        self.student=self._serializer.data['student'],
        self.course = self._serializer.data.pop('course'),
        self.consultancy= self._serializer.data.pop('consultancy'),
        self.institute = self._serializer.data.pop('institute'),
        self._get_instance()
        if self.consultancy[0]:
            data = {
                'student':self.student_instant,
                'course' :self.course_instant,
                'institute' : self.institute_instance,
                'consultancy' : self.consultancy_instance
            }
        else:
            data = {
                'student':self.student_instant,
                'course' :self.course_instant,
                'institute' : self.institute_instance
            }
        InstituteApply.objects.create(
            **data
        )

    def _get_instance(self):
        try:
            self.student_instant = StudentModel.objects.get(pk=str(self.student[0]))
        except StudentModel.DoesNotExist:
            raise StudentModelNotFound

        try:
            self.course_instant = InstituteCourse.objects.get(pk=str(self.course[0]))
        except InstituteCourse.DoesNotExist:
            raise CourseNotFound

        try:
            self.institute_instance = Institute.objects.get(pk = str(self.institute[0]))

        except Institute.DoesNotExist:
            raise InstituteNotFound

        try:
            if self.consultancy[0]:
                self.consultancy_instance = Consultancy.objects.get(pk = str(self.consultancy[0]))
            else:
                self.consultancy_instance = ""

        except Consultancy.DoesNotExist:
            raise InstituteNotFound

class ListStudentApplicationCourseUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._apply

    def _factory(self):
        self._apply = InstituteApply.objects.filter(institute=self._institute)

            

class GetApplyInstitute(BaseUseCase):
    def __init__(self,apply_id):
        self.apply_id =apply_id

    def execute(self):
        self._factory()
        return self._apply

    def _factory(self):
        try:
            self._apply = InstituteApply.objects.get(pk = self.apply_id)

        except InstituteApply.DoesNotExist:
            raise InstituteApplyNotFound

class CancleStudentApplicationUseCase(BaseUseCase):
    def __init__(self,application,serializer):
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
            # created_at__range=["2021-12-01", "2022-01-31"]
            ).values('action').annotate(Count('action'))


class SendedDocumentByStudent():
    def __init__(self,data,student,course):
        self._data = data
        self._student = student
        self.course= course
    def execute(self):
        self._factory()
    def _factory(self):
        # self.course = ""
        self.academic=[]
        self.essay =[]
        self.sop=[]
        self.lor=[]
        self.student_identity = {}
        # if len(self._data["courseId"])>1:
        #     try:
        #         self.course = InstituteCourse.objects.get(id=self._data['courseId'])
        #     except InstituteCourse.DoesNotExist:
        #         raise CourseNotFound

        for k in self._data.keys():  
            if k =="student_identity":
                c = self._data[k]['citizenship']
                if len(self._data[k]['citizenship'])>1:
                    try:
                        citizenship = Citizenship.objects.get(pk=self._data[k]['citizenship'])
                        self.student_identity["citizenship"]=citizenship
                    except Citizenship.DoesNotExist:
                        raise ValidationError({'error': _('Citizenship  does not exist for following id.')})

                if len(self._data[k]['passport'])>1:
                    try:
                        passport = Passport.objects.get(pk=self._data[k]['passport'])
                        self.student_identity["passport"]=passport
                    except Passport.DoesNotExist:
                        raise ValidationError({'error': _('Passport does not exist for following id')})

            elif k == "essay":
                if len(self._data[k])>0:
                    for essay_id in self._data[k]:
                        print("essay id",essay_id)
                        try:
                            getessay = PersonalEssay.objects.get(pk=essay_id)
                            
                            self.essay.append(AccessStudentEssay(
                                essay=getessay,
                                student=self._student,
                                course=self.course))
                        except PersonalEssay.DoesNotExist:
                            raise ValidationError({'error': _('Essay does not exist for following id')})
            
            elif k == "sop":
                if len(self._data[k])>0:
                    for sop_id in self._data[k]:
                        try:
                            getSop = StudentSop.objects.get(pk=sop_id)
                    
                            self.sop.append(AccessStudentSop(
                                sop=getSop,
                                student=self._student,
                                course=self.course
                            ))
                        except StudentSop.DoesNotExist:
                            raise ValidationError({'error': _('Passport does not exist for following id')})
            
            elif k == "lor":
                if len(self._data[k])>0:
                    for lor_id in self._data[k]:
                        try:
                            getLor = StudentLor.objects.get(pk=lor_id)
                            self.lor.append(AccessStudentLor(
                                lor=getLor,
                                student=self._student,
                                course=self.course))
                        except StudentLor.DoesNotExist:
                            raise ValidationError({'error': _('Passport does not exist for following id')})
            elif k == "academic":
                if len(self._data[k])>0:
                    for academic_id in self._data[k]:
                        try:
                            getAcademic = Academic.objects.get(pk=academic_id)
                        
                            self.academic.append(AccessOfAcademicDocument(
                                academic=getAcademic,
                                student=self._student,
                                course=self.course))
                        except StudentLor.DoesNotExist:
                            raise ValidationError({'error': _('academic does not exist for following id')})
        self._AddDataIntoTable()

    def _AddDataIntoTable(self):
        if len(self.student_identity) >0:
            citinzinship = None if self.student_identity.get('citizenship') is None else self.student_identity['citizenship']
            passport = None if self.student_identity.get('passport') is None else self.student_identity['passport']
            AccessStudentIdentity.objects.create(
                    course=self.course,
                    student=self._student,
                    citizenship=citinzinship,
                    passport = passport
                )
        if len(self.lor)>0:
            AccessStudentLor.objects.bulk_create(
                    self.lor
                )

        if len(self.sop)>0:
            AccessStudentSop.objects.bulk_create(
                    self.sop
                )
            
        if len(self.essay)>0:
            AccessStudentEssay.objects.bulk_create(
                    self.essay
                )

        if len(self.academic)>0:
            AccessOfAcademicDocument.objects.bulk_create(
                    self.academic
                )
            
class GetAccessDocument():
    # https: // docs.djangoproject.com / en / 4.0 / topics / db / sql /
    # https: // anthonydebarros.com / 2020 / 0
    # 9 / 06 / generate - json -
    # from
    # -sql - using - python /
    def __init__(self,student,course):
        self.studentId=student
        self.courseId=course

    def execute(self):
        return self._factory()

    def _factory(self):
        # self.studentId='a6586b1f-7b2b-433c-be48-1711c4770fae'
        # self.courseId= 'dd26af6f-4ace-4660-9b67-6db5dad5c4bb'
        self._GetSop()
        self._GetStudentIdentity()
        self._GetPersonalEsay()
        self._GetAcademicDetail()
        self._GetStudentLor()
        self._GetStudentDetail()
        data={
            "student":self.student,
            "sop":self.sop,
            "lor":self.lor,
            "academic_detail":self.academic,
            "essay":self.personal_essay,
            "student_identity":self.identity
        }
        return data
    def _GetStudentDetail(self):
        get_student ="""
        select * from public.students_studentmodel left join 
        public.students_studentaddress on 
        students_studentmodel.id=students_studentaddress.student_id
        where students_studentmodel.id='{student_id}'
        """.format(student_id=self.studentId)

        self.student=QueryDataSerializer(query_data=get_student).execute()
    def _GetSop(self):
        get_sop_query = """
        select academic_studentsop.document,academic_studentsop.id,academic_studentsop.doc_type,institute_course_accessstudentsop.id
        as access_id
        from  public.institute_course_accessstudentsop 
        inner Join public.academic_studentsop
        on academic_studentsop.id=institute_course_accessstudentsop.sop_id
        where institute_course_accessstudentsop.student_id='{student_id}'
        and institute_course_accessstudentsop.course_id='{course_id}'
        """.format(course_id=self.courseId,student_id=self.studentId)

        self.sop=QueryDataSerializer(query_data=get_sop_query).execute()

    def _GetStudentIdentity(self):
        student_identity_query = """
        select public."studentIdentity_citizenship".front_page,
        public."studentIdentity_citizenship".back_page,
        public."studentIdentity_citizenship".citizenship_number,
        public."studentIdentity_citizenship".issue_date,
        public."studentIdentity_citizenship".issue_from,
        institute_course_accessstudentidentity.id ,
        public."studentIdentity_passport".id as p_id,
        public."studentIdentity_citizenship".id as c_id,
        public."studentIdentity_passport".passport_number ,
        public."studentIdentity_passport".issue_date as passport_issue_data,
        public."studentIdentity_passport".expire_date as passport_expire_date,
        public."studentIdentity_passport".issue_from as passport_issue_from,
        public."studentIdentity_passport".passport_image
        from  public.institute_course_accessstudentidentity 
        right Join public."studentIdentity_citizenship"
        on public."studentIdentity_citizenship".id=
        institute_course_accessstudentidentity.citizenship_id
        right join public."studentIdentity_passport" on
        public."studentIdentity_passport".id=institute_course_accessstudentidentity.passport_id
        where institute_course_accessstudentidentity.student_id='{student_id}'
        and institute_course_accessstudentidentity.course_id='{course_id}' ;
        """.format(student_id=self.studentId,course_id=self.courseId)
        self.identity = QueryDataSerializer(query_data=student_identity_query).execute()

    def _GetStudentLor(self):
        lor_query = """
            select academic_studentlor.document,
            academic_studentlor.doc_type,
            academic_studentlor.name from  public.institute_course_accessstudentlor
            inner join public.academic_studentlor on
            public.institute_course_accessstudentlor.lor_id=academic_studentlor.id
            where institute_course_accessstudentlor.student_id='{student_id}' and
            institute_course_accessstudentlor.course_id='{course_id}';

        """.format(student_id=self.studentId,course_id=self.courseId)
        self.lor = QueryDataSerializer(query_data=lor_query).execute()

    def _GetPersonalEsay(self):
        essay_query = """
        select academic_personalessay.name,
        academic_personalessay.content,
        academic_personalessay.doc_type,
        academic_personalessay.essay,
        institute_course_accessstudentessay.essay_id from public.institute_course_accessstudentessay
        inner join public.academic_personalessay on
        academic_personalessay.id=institute_course_accessstudentessay.essay_id
        where institute_course_accessstudentessay.course_id='{course_id}'
        and
        institute_course_accessstudentessay.student_id='{student_id}'
        """.format(course_id=self.courseId,student_id=self.studentId)
        self.personal_essay = QueryDataSerializer(query_data=essay_query).execute()

    def _GetAcademicDetail(self):
        academic_query = """
        select * from  institute_course_accessofacademicdocument
        inner join academic_academic on 
        academic_academic.id=institute_course_accessofacademicdocument.academic_id
        where institute_course_accessofacademicdocument.course_id='{course_id}' and
        institute_course_accessofacademicdocument.student_id='{student_id}'
        """.format(course_id=self.courseId,student_id=self.studentId)
        self.academic = QueryDataSerializer(query_data=academic_query).execute()

        


class CompareInstituteCourseUseCase(BaseUseCase):
    def __init__(self,course):
        self._course = course

    def execute(self):
        self._factory()
        return self._institute_course

    def _factory(self):
        self._institute_course = InstituteCourse.objects.filter(pk=self._course).prefetch_related("institute")





# query = """
#             select * from public.students_studentmodel
#             FULL OUTER JOIN public.institute_course_accessstudentsop
#             ON institute_course_accessstudentsop.student_id=students_studentmodel.id AND
#             institute_course_accessstudentsop.course_id='{course_id}'
#             FULL OUTER Join public.academic_studentsop
#             on academic_studentsop.id=institute_course_accessstudentsop.sop_id
#             FULL OUTER join public.institute_course_accessstudentessay
#             on institute_course_accessstudentessay.course_id='{course_id}'
#             And institute_course_accessstudentessay.student_id=students_studentmodel.id
#             FULL OUTER join public.academic_personalessay
#             on academic_personalessay.id=institute_course_accessstudentessay.essay_id
#             FULL OUTER join public.institute_course_accessstudentidentity
#             on institute_course_accessstudentidentity.student_id=students_studentmodel.id and
#             institute_course_accessstudentidentity.course_id='{course_id}'
#             FULL OUTER join public."studentIdentity_citizenship" on
#             public."studentIdentity_citizenship".id=institute_course_accessstudentidentity.citizenship_id
#             FULL OUTER join public."studentIdentity_passport" on
#             public."studentIdentity_passport".id=institute_course_accessstudentidentity.passport_id
#             FULL OUTER join public.institute_course_accessstudentlor on
#             institute_course_accessstudentlor.student_id=students_studentmodel.id and
#             institute_course_accessstudentlor.course_id='{course_id}'
#             FULL OUTER join public.academic_studentlor on
#             academic_studentlor.id = institute_course_accessstudentlor.lor_id
#             FULL OUTER join public.institute_course_accessofacademicdocument on
#             institute_course_accessofacademicdocument.student_id=students_studentmodel.id and
#             institute_course_accessofacademicdocument.course_id='{course_id}'
#             FULL OUTER join public.academic_academic on
#             academic_academic.id=institute_course_accessofacademicdocument.academic_id
#             where students_studentmodel.id='{student_id}'
#         """.format(course_id=courseId,student_id=studentId)

