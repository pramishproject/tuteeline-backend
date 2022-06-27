from datetime import datetime
import time

from apps.core.usecases import BaseUseCase
from apps.counselling.exception import AlreadyBooked, TimeError, CourseDoesntExist
from apps.counselling.models import InstituteCounselling, InterestedCourse, ConsultancyCounselling
from apps.institute_course.models import InstituteCourse
from apps.utils.string_to_json import StringToJson
from apps.students.models import StudentModel
from apps.utils.uuid_validation import is_valid_uuid


class CreateInstituteCounsellingUseCase(BaseUseCase):
    def __init__(self,student:StudentModel,serializer):
        self._student = student
        self._data = serializer.validated_data

    def execute(self):

        self._factory()

    def _factory(self):
        interested_courses_list = self._data.pop('interested_courses')
        counselling_time = self._data.get("which_time")
        now = datetime.now()
        if time.mktime(now.timetuple())<time.mktime(counselling_time.timetuple()):
            councilinglist =InstituteCounselling.objects.filter(student=self._student,institute=self._data.get("institute")
                                                                ,which_time__range=[now,counselling_time]).first()
            if councilinglist is None:
                counciling =InstituteCounselling.objects.create(
                    student=self._student,
                    **self._data
                )
                bulk_interested_course = []
                for courseId  in interested_courses_list:
                    if is_valid_uuid(courseId):
                        try:
                            course = InstituteCourse.objects.get(pk=courseId) #todo add institute to filter course
                            bulk_interested_course.append(InterestedCourse(
                                counselling= counciling,
                                course = course
                            ))
                        except InstituteCourse.DoesNotExist:
                            raise CourseDoesntExist

                if len(bulk_interested_course)>0:
                    InterestedCourse.objects.bulk_create(bulk_interested_course)
            #
            else:
                raise AlreadyBooked
        else:
            raise TimeError



class GetCounselling(BaseUseCase):
    def __init__(self,counselling_id):
        self._counselling_id = counselling_id

    def execute(self):
        self._factory()
        return self._counselling

    def _factory(self):
        self._counselling = InstituteCounselling.objects.get(pk=self._counselling_id)

class ListStudentCounsellingUseCase(BaseUseCase):
    def __init__(self,student:StudentModel):
        self._student = student

    def execute(self):
        self._factory()
        return self._counselling

    def _factory(self):
        self._counselling = InstituteCounselling.objects.filter(student=self._student).prefetch_related("institute")


class ListStudentCounsellingForInstituteUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute=institute

    def execute(self):
        self._factory()
        return self._counselling

    def _factory(self):
        self._counselling =InstituteCounselling.objects.filter(institute=self._institute).prefetch_related("student","assign_to")


class AssignCounselorUseCase(BaseUseCase):
    def __init__(self,counselling,serializer):
        self._counselling = counselling
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._counselling,key,self._data.get(key))

        self._counselling.updated_at = datetime.now()
        self._counselling.save()

class ListCounselingInstituteStaffUseCase(BaseUseCase):
    def __init__(self,staff):
        self._staff = staff

    def execute(self):
        self._factory()
        return self._counselling

    def _factory(self):
        self._counselling = InstituteCounselling.objects.filter(assign_to=self._staff).\
            prefetch_related('student')
# consultancy----------------------------------

class CreateConsultancyCounsellingUseCase(BaseUseCase):
    def __init__(self,student,serializer):
        self._student = student
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        counselling_time = self._data.get("which_time")
        now = datetime.now()
        if time.mktime(now.timetuple()) < time.mktime(counselling_time.timetuple()):
            schedule_isexist = ConsultancyCounselling.objects.filter(student=self._student,
                                                                 consultancy=self._data.get("consultancy")
                                                                 , which_time__range=[now, counselling_time]).exists()
            if schedule_isexist:
                raise AlreadyBooked
            else:
                ConsultancyCounselling.objects.create(
                    student=self._student,
                    **self._data
                )
        else:
            raise TimeError

