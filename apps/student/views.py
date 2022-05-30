import uuid
from collections import OrderedDict

from apps.college.User.utils.token import generate_access_token, generate_refresh_token
from apps.college.serializers import CommentSerializer, CouncilorSerializer
from apps.core.decorators import student_required
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework import exceptions
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.college.models import College, CourceDetail, CounselorModel
from .models import LORModel, PassportModel, Student, AcademicInfo, Eligibility, Parents, Bookmark, VisitedCollege, \
    StudentApply, StudentEssay, Comment, CitizenshipModel
from .serializers import AcademicCertificateSerializer, AcademicMarksheetSerializer, StudentUpdateSerializer, \
    EligibilitySerializer, UpdateUserSerializer
from .serializers import LorSerializer, PassportSerializer, CitizenshipSerializer, UserCreateCustomSerializer, \
    StudentSerializer, UserSerializer, AcademicSerializer, AcademicUpdateSerializer, ParentsSerializer
from .serializers import StudentProfileUpdate, UpdateStudentAction, StudentEssayUpdateSerializer, \
    StudentEssaySerializer, GetApplyDataSerializer, EligibilityCertificateSerializer, StudentApplySerializer, \
    BookmarkSerializer, BookmarkGetCollegeSerializer, VisitedCollegeSerializer
from ..notification.mixins import NotificationMixin

User = get_user_model()


# Create your views here.
@permission_classes((permissions.AllowAny,))
class StudentsCreateAccountApi(APIView):
    def post(self, request):
        student = OrderedDict()
        student.update(request.data)
        password1 = student['password1']
        password2 = student['password2']
        student._mutable = True
        print(student._mutable)
        if password1 == password2:
            serializer = UserCreateCustomSerializer(data=student)
            if serializer.is_valid():
                userser = UserSerializer(data={"email": student['email'], "password": password1})
                if userser.is_valid():
                    user = User.objects.create_user(email=userser.data['email'], password=password1,
                                                    first_name=student['first_name'], is_student=True,
                                                    last_name=student['last_name'], middle_name=student['middle_name'])
                    user.save()
                    student['id'] = user.id
                    print("*******************type", student, type(user.id))
                    profileSerializer = StudentSerializer(data=student)
                    if profileSerializer.is_valid():
                        profileSerializer.save()
                        return Response(profileSerializer.data)
                    else:
                        return Response({"message": profileSerializer.errors})
                else:
                    return Response({"message": userser.errors})
            else:
                return Response({"message": serializer.errors})
        else:
            return Response({'message': 'password not match'}, status=406)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        data = OrderedDict()
        data.update(request.data)
        password1 = data['password1']
        password2 = data['password2']
        email = request.user.email
        password = data['password']
        print(email)
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            if password1 == password2:
                user.set_password(password1)
                user.save()
                return Response({"message": "password change successfully", "error": False})
            else:
                return Response({"message": "password1 and password 2 is not match", "error": True}, status=404)

        return Response({'message': "user not match", "error": True}, status=400)


@permission_classes((permissions.AllowAny,))
class ChangeStudentProfile(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        try:
            sid = request.user.id
            student = Student.objects.get(id=sid)
            serializer = StudentProfileUpdate(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=422)

        except Student.DoesNotExist:
            return Response({'message': 'doesnt exist'})


@permission_classes((permissions.AllowAny,))
class StudentLoginApi(APIView):
    def post(self, request):
        data = request.data
        print(data)
        email = data['email']
        password = data['password']

        response = Response()
        if (not email) or (not password):
            raise exceptions.AuthenticationFailed('username and password required')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')

        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
        print("user", user)
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        return response

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def delete(self, request):
        email = request.data['email']
        password = request.data['password']
        if (not email) or (not password):
            raise exceptions.AuthenticationFailed('username and password required')
        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
        else:
            fromtokenid = request.user.id
            fromuserid = user.id
            if fromtokenid == fromuserid:
                user.delete()
                return Response({'message': 'delete successful', 'statue': True})
            else:
                return Response({'message': 'id is not match', 'statue': False})


@permission_classes((permissions.AllowAny,))
class GetStudentDataApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        user = request.user
        id = user.id
        first_name = user.first_name
        middle_name = user.middle_name
        last_name = user.last_name
        student = Student.objects.get(id=id)
        serializer = StudentSerializer(student)
        student = serializer.data
        student['first_name'] = first_name
        student['middle_name'] = middle_name
        student['last_name'] = last_name
        academic = AcademicInfo.objects.filter(student=id)
        test = Eligibility.objects.filter(student=id)
        citizenship = CitizenshipModel.objects.filter(id=id).first()
        citizenshipSerializer = CitizenshipSerializer(citizenship)
        academicser = AcademicSerializer(academic, many=True)
        testserializer = EligibilitySerializer(test, many=True)
        student['academic'] = academicser.data
        student['eligibility'] = testserializer.data
        student['citizenship'] = citizenshipSerializer.data
        schoolDoc = False
        highschoolDoc = False
        undergraduateDoc = False
        postgraduateDoc = False
        graduateDoc = False
        sop = False
        passport = False
        citizenship = False
        for i in academic:
            if i.level == 'Graduate':
                graduateDoc = True
            elif i.level == "High School":
                highschoolDoc = True
            elif i.level == "Undergraduate":
                undergraduateDoc = True
            elif i.level == "School":
                schoolDoc = True
            elif i.level == "Post Graduate":
                postgraduateDoc = True
        if citizenshipSerializer.data['id'] is not None:
            citizenship = True

        student['available_document'] = {"passport": passport, "citizenship": citizenship,
                                         "postgraduateDoc": postgraduateDoc,
                                         "graduateDoc": graduateDoc, "sop": sop, "schoolDoc": schoolDoc,
                                         "highschoolDoc": highschoolDoc, "undergraduateDoc": undergraduateDoc,
                                         "citizenship": citizenship}
        return Response(student)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        student = request.data
        id = request.user.id
        userdata = User.objects.get(id=id)
        userdata.first_name = student['first_name']
        userdata.middle_name = student['middle_name']
        userdata.last_name = student['last_name']

        findstd = Student.objects.get(id=id)
        user_serializer = UpdateUserSerializer(data=student)
        serializer = StudentUpdateSerializer(findstd, data=student)
        if serializer.is_valid() and user_serializer.is_valid():
            serializer.save()
            userdata.save()
            serializedata = serializer.data
            serializedata['first_name'] = student['first_name']
            serializedata['middle_name'] = student['middle_name']
            serializedata['last_name'] = student['last_name']
            return Response(serializedata)
        else:
            return Response(serializer.errors, status=404)


@permission_classes((permissions.AllowAny,))
class InitApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        id = request.user.id

        #    "picture":picture,"passport":passport,"citizenship":citizenship,"postgraduateDoc":postgraduateDoc,"graduateDoc":graduateDoc,"sop":sop,"profile":profile,"schoolDoc":schoolDoc,"highschoolDoc":highschoolDoc,"undergraduateDoc":undergraduateDoc,

        return Response({'first_name': request.user.first_name, 'middle_name': request.user.middle_name,
                         'last_name': request.user.last_name, 'id': request.user.id})


@permission_classes((permissions.AllowAny,))
class AcademicApi(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def post(self, request):
        uid = request.user.id
        print(request.data)
        data = AcademicInfo.objects.filter(student=uid, level=request.data['level']).exists()
        if data:
            return Response({'message': 'this grade academic detail already exist'}, status=409)
        else:
            data = OrderedDict()
            data.update(request.data)
            data['student'] = uid
            if 'percentage' in data:
                per = float(data['percentage'])
                data['outof'] = 100
                data['percentage'] = per

            elif 'gpa' in data:
                gpa = float(float(data['gpa']) / int(data['total_gpa'])) * 100
                data['outof'] = int(data['total_gpa'])
                data['percentage'] = gpa
            else:
                data['percentage'] = 0
            serializer = AcademicSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=409)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        data = OrderedDict()
        data.update(request.data)
        user = request.user
        data = request.data
        id = data['id']
        sid = user.id
        student = AcademicInfo.objects.get(id=id, student=sid)
        print(student)
        serializer = AcademicUpdateSerializer(student, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=422)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def delete(self, request):
        sid = request.user.id
        id = request.GET.get('id')
        if id:
            academic = AcademicInfo.objects.get(id=id, student=sid)
            if academic is not None:
                academic.delete()
                return Response({'message': 'delete successfully'})
            else:
                return Response({'message': 'data not exist'}, status=400)
        else:
            return Response({'message': 'null not exist'}, status=400)


@permission_classes((permissions.AllowAny,))
class DocumentApi(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        try:
            user = request.user
            data = request.data
            sid = user.id
            modeldir = "student"
            id = data['id']

            student = AcademicInfo.objects.get(id=id, student=sid)
            if 'certificate' in data:
                serializer = AcademicCertificateSerializer(student, data=data)

            elif 'marksheet' in data:
                serializer = AcademicMarksheetSerializer(student, data=data)
            else:
                return Response({"message": "not match"}, status=400)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except AcademicInfo.DoesNotExist:
            return Response({'message': "not exist"}, status=400)


@permission_classes((permissions.AllowAny,))
class EligibilityExamApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def post(self, request):
        data = OrderedDict()
        data.update(request.data)
        sid = request.user.id
        data['student'] = sid
        eligibility = Eligibility.objects.filter(student=sid,
                                                 eligibility_exam_name=data['eligibility_exam_name']).first()
        if eligibility is None:
            serializer = EligibilitySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'message': 'already exist'}, status=400)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        try:
            data = request.data
            sid = request.user.id
            modeldir = "student"
            if data['type'] == 'certificate':
                updatedata = Eligibility.objects.get(id=data['id'], student=sid)
                serializer = EligibilityCertificateSerializer(updatedata, {'certificate': data['certificate']})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({'error': 1}, status=422)
            elif data['type'] == 'data':
                updatedata = Eligibility.objects.get(id=data['id'], student=sid)
                updatedata.score = data['score']
                print(updatedata.Score)
                updatedata.save()
                return Response({'Score': updatedata.Score})
            else:
                return Response({'message': 'type not exist'}, status=400)
        except Eligibility.DoesNotExist:
            return Response({'message': 'id doesnt exist'}, status=400)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def delete(self, request):
        sid = request.user.id
        eligibility = Eligibility.objects.get(id=request.GET.get('id'), student=sid)
        eligibility.delete()
        return Response({'message': 'delete success'})


@permission_classes((permissions.AllowAny,))
class ApplyAPI(APIView, NotificationMixin):
    notification_group = ['portal_user']

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def post(self, request):
        try:
            data = OrderedDict()
            data.update(request.data)
            sid = request.user.id
            cid = uuid.UUID(data['college'])
            college = College.objects.get(id=cid)
            data['college'] = cid
            data['student'] = sid
            data['first_name'] = request.user.first_name
            data['middle_name'] = request.user.middle_name
            data['last_name'] = request.user.last_name
            data['applyed'] = True
            # course=data['course']
            print(data)
            findcourse = CourceDetail.objects.filter(id=data['course_id'], college=cid).first()
            if findcourse is None:
                return Response({"message": "course is not exist"}, status=404)
            else:
                serializer = StudentApplySerializer(data=data)
                print(serializer.is_valid())
                if serializer.is_valid():
                    serializer.save()
                    # send notification
                    data = {
                        'name': 'Student Applied',
                        'image': request.user.student.photo.url,
                        'content': 'Student Applied to College: {}.'.format(college.name),
                        'id': str(request.user.student.id)
                    }
                    self.send_notification(data=data)
                    return Response(serializer.data)
                else:
                    return Response({'error': serializer.errors})
        except College.DoesNotExist:
            return Response({'message': 'college Doesnt Exist'}, status=404)


    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        try:
            sid = request.user.id
            data = StudentApply.objects.select_related("college").filter(student=sid)
            apply = GetApplyDataSerializer(data, many=True)
            return Response(apply.data)
        except StudentApply.DoesNotExist:
            return Response({'message': 'not exist'}, status=404)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        try:
            sid = request.user.id
            cid = uuid.UUID(request.data['college'])
            print(cid)
            apply = StudentApply.objects.filter(student=sid, college=cid).first()
            serializer = UpdateStudentAction(apply, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
                # return Response({'message':1})
            else:
                return Response(serializer.errors, status=409)
        except StudentApply.DoesNotExist:
            return Response({'message': 'not exist'}, status=404)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def delete(self, request):
        try:
            sid = request.user.id
            id = request.GET.get('id')
            apply = StudentApply.objects.get(id=id, student=sid)
            apply.delete()
            return Response({'message': 'delete'})
        except StudentApply.DoesNotExist:
            return Response({'message': 'not exist'}, status=404)


@permission_classes((permissions.AllowAny,))
class ParentsView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def post(self, request):
        sid = request.user.id
        data = OrderedDict()
        data.update(request.data)
        data['student'] = sid
        serializer = ParentsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'error': serializer.errors}, status=406)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        student = request.user.id
        find = Parents.objects.filter(student=student)
        serializer = ParentsSerializer(find, many=True)
        return Response(serializer.data)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        try:
            data = OrderedDict()
            data.update(request.data)
            id = data['id']
            student = request.user.id
            getparents = Parents.objects.get(id=id, student=student)
            data['student'] = student
            serializer = ParentsSerializer(getparents, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Parents.DoesNotExist:
            return Response({'message': "not exist"}, status=404)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def delete(self, request):
        sid = request.user.id
        parents = Parents.objects.get(id=request.GET.get('id'), student=sid)
        parents.delete()
        return Response({'message': 'delete success'})


@permission_classes((permissions.AllowAny,))
class EssayAPI(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def post(self, request):
        data = OrderedDict()
        data.update(request.data)
        id = request.user.id
        data['id'] = id
        serializer = StudentEssaySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=422)
        # return Response({'message':12})

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        try:
            id = request.user.id
            essay = StudentEssay.objects.get(id=id)
            serializer = StudentEssaySerializer(essay)
            return Response(serializer.data)
        except StudentEssay.DoesNotExist:
            return Response({'noexist': True})

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        try:
            id = request.user.id
            essay = StudentEssay.objects.get(id=id)
            data = request.data
            serializer = StudentEssayUpdateSerializer(essay, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=422)
        except StudentEssay.DoesNotExist:
            return Response({'message': 'doesnt exist'}, status=404)


@permission_classes((permissions.AllowAny,))
class CitizensipApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        try:
            cid = request.user.id
            citizenship = CitizenshipModel.objects.get(id=cid)
            serializer = CitizenshipSerializer(citizenship)
            data = dict(serializer.data)
            data.update({'exist': True})
            return Response(data)
        except CitizenshipModel.DoesNotExist:
            return Response({'message': 'data doesnt exist', 'exist': False}, status=404)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def post(self, request):
        cid = request.user.id
        data = OrderedDict()
        data.update(request.data)
        data.update({'id': cid})
        serializer = CitizenshipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        # return Response({'s':1})

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        cid = request.user.id
        data = OrderedDict()
        data.update(request.data)
        data.update({'id': cid})
        find = CitizenshipModel.objects.get(id=cid)
        serializer = CitizenshipSerializer(find, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@permission_classes((permissions.AllowAny,))
class PassportAPI(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        try:
            print("serializer****************", request.user.id)
            passport = PassportModel.objects.get(id=request.user.id)
            serializer = PassportSerializer(passport)
            print("serializer", serializer.data)
            data = dict(serializer.data)
            data.update({'exist': True})
            return Response(data)
        except PassportModel.DoesNotExist:
            return Response({"message": "not exist", "error": True}, status=400)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def post(self, request):
        cid = request.user.id
        data = OrderedDict()
        data.update(request.data)
        data.update({'id': cid})
        serializer = PassportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        cid = request.user.id
        data = OrderedDict()
        data.update(request.data)
        data.update({'id': cid})
        find = PassportModel.objects.get(id=cid)
        serializer = PassportSerializer(find, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@permission_classes((permissions.AllowAny,))
class StudentLORApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        try:
            sid = request.user.id
            data = LORModel.objects.filter(student=sid)

            serializer = LorSerializer(data, many=True)
            data = serializer.data

            return Response(data)
        except LORModel.DoesNotExist:
            return Response({"message": "doesnt exist", "exist": False}, status=400)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def post(self, request):
        sid = request.user.id
        data = OrderedDict()
        data.update(request.data)
        data.update({"student": sid})
        serializer = LorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=409)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def put(self, request):
        try:
            sid = request.user.id
            lorid = request.GET.get('lorid')
            data = OrderedDict()
            data.update(request.data)
            find = LORModel.objects.get(student=sid, id=lorid)
            data.update({"student": sid})
            serializer = LorSerializer(find, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except LORModel.DoesNotExist:
            return Response({"message": "not exist", "exist": False}, status=404)

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def delete(self, request):
        try:
            sid = request.user.id
            lorid = request.GET.get('lorid')
            lor = LORModel.objects.get(student=sid, id=lorid)
            lor.delete()
            return Response({"message": "delete LOR Successfully"})
        except LORModel.DoesNotExist:
            return Response({"message": "not exist", "exist": False}, status=404)


@permission_classes((permissions.AllowAny,))
class BookmarkApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def post(self, request):
        sid = request.user.id
        # print(uuid.UUID(request.GET.get('cid')))
        college = request.data['cid']
        findbookmark = Bookmark.objects.filter(student=sid, college=uuid.UUID(college)).first()
        if findbookmark is None:
            bookmark = BookmarkSerializer(data={"student": sid, "college": uuid.UUID(college)})
            if bookmark.is_valid():
                bookmark.save()
                return Response({"message": "bookmark"})
            else:
                return Response(bookmark.errors)
        else:
            return Response({'message': 'already exist'})

    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        sid = request.user.id
        data = Bookmark.objects.select_related("college").filter(student=sid)
        bookemark = BookmarkGetCollegeSerializer(data, many=True)
        return Response(bookemark.data)


class VisitCollegeApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        sid = request.user.id
        data = VisitedCollege.objects.select_related().filter(student=sid)
        print(data)
        serializer = VisitedCollegeSerializer(data, many=True)
        return Response(serializer.data)


# @permission_classes((permissions.AllowAny,))
# class SOPAPIViews(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     permission_classes = [IsAuthenticated]
#     @method_decorator([ student_required], name='dispatch')
#     def post(self,request):
#         data=OrderedDict()
#         data.update(request.data)
#         data.update({"student":request.user.id})
#         serializer=SOPSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


#     permission_classes = [IsAuthenticated]
#     @method_decorator([ student_required], name='dispatch')
#     def put(self,request):
#         data=OrderedDict()
#         data.update(request.data)
#         data.update({"student":request.user.id})
#         sopid=request.GET.get('sopid')
#         find=StudentSOP.objects.get(student=request.user.id,id=sopid)
#         serializer=SOPSerializer(find,data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     permission_classes = [IsAuthenticated]
#     @method_decorator([ student_required], name='dispatch')
#     def get(self,request):
#         sid=request.user.id
#         sop=StudentSOP.objects.filter(student=sid)
#         serializer=SOPSerializer(sop,many=True)
#         return Response(serializer.data)


#     permission_classes = [IsAuthenticated]
#     @method_decorator([ student_required], name='dispatch')
#     def delete(self,request):   
#         sopid=request.GET.get('sopid')
#         sid=request.user.id
#         sop=StudentSOP.objects.get(student=sid,id=sopid)
#         sop.delete()
#         return Response({"message":"sop delete successfully"})


@permission_classes((permissions.AllowAny,))
class StudentApplicationComment(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([student_required], name='dispatch')
    def get(self, request):
        aid = request.GET.get('id')  # application id
        comment = Comment.objects.filter(apply=aid)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class StudentCouncilorView(APIView):
    def get(self, request):
        cid = request.GET.get('college_id')
        cid = uuid.UUID(cid)
        councilor = CounselorModel.objects.filter(college=cid)
        serializer = CouncilorSerializer(councilor, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class Test(APIView):
    def post(self, request, name):
        print(name)
        return Response({'message': 1})
