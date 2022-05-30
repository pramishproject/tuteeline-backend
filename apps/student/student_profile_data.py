from django.contrib.auth import get_user_model

from apps.student.models import Student, AcademicInfo, Eligibility, Parents, CitizenshipModel, PassportModel, LORModel, \
    StudentEssay
from apps.student.serializers import ParentsSerializer, CitizenshipSerializer, PassportSerializer, LorSerializer, \
    StudentEssaySerializer, StudentApplicationDetailSerializer, AcademicSerializer, EligibilitySerializer

User = get_user_model()


def get_student_detail(id):
    # id=uuid.UUID(data['student'])
    user = User.objects.get(id=id)

    first_name = user.first_name
    middle_name = user.middle_name
    last_name = user.last_name
    student = Student.objects.get(id=id)
    serializer = StudentApplicationDetailSerializer(student)
    student = serializer.data
    student['first_name'] = first_name
    student['middle_name'] = middle_name
    student['last_name'] = last_name
    academic = AcademicInfo.objects.filter(student=id)
    test = Eligibility.objects.filter(student=id)
    parents = Parents.objects.filter(student=id)
    parentsserializer = ParentsSerializer(parents, many=True)
    Citizenship = CitizenshipModel.objects.filter(id=id)
    citizenshipSer = CitizenshipSerializer(Citizenship, many=True)
    passport = PassportModel.objects.filter(id=id)
    passportSer = PassportSerializer(passport, many=True)
    lor = LORModel.objects.filter(student=id)
    lorserializer = LorSerializer(lor, many=True)
    essay = StudentEssay.objects.filter(id=id)
    essaySer = StudentEssaySerializer(essay, many=True)
    academicser = AcademicSerializer(academic, many=True)
    testserializer = EligibilitySerializer(test, many=True)
    student['academic'] = academicser.data
    student['eligibility'] = testserializer.data
    student['parents'] = parentsserializer.data
    student['citizenship'] = citizenshipSer.data
    student['passport'] = passportSer.data
    student['lor'] = lorserializer.data
    student['essay'] = essaySer.data

    return student

#     {
#     "id": 2,
#     "course": "Be civil",
#     "first_name": "pramish",
#     "middle_name": "",
#     "last_name": "karki",
#     "status": "0",
#     "applyed": true,
#     "view_date": "2021-08-17T08:02:06.858695",
#     "action_date": "2021-08-17T08:02:06.858713",
#     "apply_date": "2021-08-17T08:02:06.859655",
#     "view": false,
#     "student_action": "1",
#     "form_payment": false,
#     "enrolled": false,
#     "college": "58a83b6a-b98a-44ef-ae12-c46e66e2682e",
#     "student": "e9b769f6-651b-4d2c-a7fb-41ba8a3706c6"
# }
