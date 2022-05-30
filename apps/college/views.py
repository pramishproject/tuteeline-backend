import datetime
import uuid
from collections import OrderedDict

from django.http import Http404
from geopy import Nominatim

from apps.core.decorators import college_required
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from rest_framework import exceptions
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.student.models import StudentApply, VisitedCollege, Bookmark, Comment
from apps.student.serializers import StudentApplySerializer, UpdateStatusSeializer, CollegeVisitSerializer
from .User.utils.token import generate_access_token, generate_refresh_token
from .chart import date_wise_filter, application_report_count, count_yeardata
from .models import Accomodation, College, CounselorModel, CourceDetail, Faculty, Course, Facility, Canteen, Laboratory, \
    LibraryModel, Blog
from .models import Gallery, RestrictCountry
from .serializers import AccomodationSerializer, UserSerializer, CourseDetailEditSerializer, CanteenSerializer, \
    LaboratorySerializer
from .serializers import BlogSerializer, LibrarySerializer, CommentSerializer, CollegeSerializer, CouncilorSerializer, \
    CollegeCardSerializer, CollegeDataUpdateSerializer, CollegeLogoUpdate, GetCountryRestrictedSerializer, \
    CollegeCoverpageUpdate, FacultySerializer
from .serializers import CourceDetailFormSerializer, CollegeGallertStudentpage, GallerySerializer, \
    CourceDetailInsertSerializer, LocationSerializer, AboutUpdateSerializer
from .serializers import FetchCourseSerializer, FacilitySerializer, CreateUserSerializer, \
    CheckCollegeAccountCreateSerializer, StudentStatusSerializer, RestrictCountrySerializer
from ..notification.mixins import NotificationMixin
from ..student.student_profile_data import get_student_detail

User = get_user_model()


@permission_classes((permissions.AllowAny,))
class UserRegisterApi(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        college = OrderedDict()
        college.update(request.data)

        customserializer = CheckCollegeAccountCreateSerializer(data=college)
        if customserializer.is_valid():
            if college['password1'] == college['password2']:
                password = college['password'] = college['password1']
                if college['lat'] and college['long']:
                    Latitude = college['lat']
                    Longitude = college['long']
                    geolocator = Nominatim(user_agent="geoapiExercises")
                    location = geolocator.geocode(Latitude + "," + Longitude)
                    college['location'] = str(location)
                serializer = CreateUserSerializer(data=college)
                if serializer.is_valid():
                    email = serializer.data['email']
                    user = User.objects.create_user(
                        email=email,
                        password=password,
                        is_institute=True,
                    )

                    user.save()
                    college['id'] = user.id
                    collegeserializer = CollegeSerializer(data=college)
                    if collegeserializer.is_valid():
                        collegeserializer.save()
                        return Response(collegeserializer.data)
                    else:
                        return Response(collegeserializer.errors, status=422)

                else:
                    return Response(serializer.errors, status=422)
            else:
                return Response({"message": "password not match"})

        else:
            return Response(customserializer.errors, status=400)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        data = OrderedDict()
        data.update(request.data)
        data = request.data
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", data)
        password1 = data['password1']
        # password1
        password2 = data['password2']
        email = request.user.email
        password = data['password']
        print(email)
        user = authenticate(email=email, password=password)
        print("*****", user)
        if user is not None:
            if password1 == password2:
                user.set_password(password1)
                user.save()
                return Response({"message": "password change successfully", "error": False})
            else:
                return Response({"message": "password1 and password 2 is not match", "error": True}, status=404)

        return Response({'message': "user not match", "error": True}, status=400)


@permission_classes((permissions.AllowAny,))
class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        response = Response()
        if (not email) or (not password):
            raise exceptions.AuthenticationFailed('username and password required')
        user = User.objects.filter(email=email).first()
        if (user is None):
            raise exceptions.AuthenticationFailed('user not found')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
        print(user.id)
        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        return response

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def delete(self, request):
        email = request.data['email']
        print("delete account")
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
class CollegePageApi(APIView):
    def get(self, request, page):
        college = College.objects.all()

        if len(college):
            collegepegination = Paginator(college, 18)
            pagelist = collegepegination.page(page).object_list
            serializer = CollegeCardSerializer(pagelist, many=True)
            return Response(serializer.data)
        return Response({"message": "no data found"}, status=204)


@permission_classes((permissions.AllowAny,))
class CollegeApiViews(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, id):
        try:
            return College.objects.get(id=id)
        except College.DoesNotExist:
            raise Http404

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        id = request.user.id
        college = self.get_object(id)
        serializer = CollegeSerializer(college)
        return Response(serializer.data)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request, id=None):
        print(request.data)
        # id=uuid.UUID('83831bbf-3c4c-4b1f-bba0-4db75d00485f')
        id = request.user.id
        college = self.get_object(id)
        update = request.data
        if (update['update'] == "logo"):
            serializer = CollegeLogoUpdate(college, data=update)
        elif (update['update'] == "coverpage"):
            serializer = CollegeCoverpageUpdate(college, data=update)
        elif (update['update'] == "data"):
            serializer = CollegeDataUpdateSerializer(college, data=update)
        elif (update['update'] == 'about'):
            serializer = AboutUpdateSerializer(college, data=update)
        else:
            return Response({'message': 'missing update value'}, status=404)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=404)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def delete(self, request):
        pk = request.user.id
        college = self.get_object(pk)
        college.delete()
        return Response({'message': "delete"}, status=202)


@permission_classes((permissions.AllowAny,))
class CollegeFaculty(APIView):
    def get(self, request):
        faculty = Faculty.objects.all()
        if len(faculty) > 0:
            serializer = FacultySerializer(faculty, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'empty'}, status=404)


@permission_classes((permissions.AllowAny,))
class CollegeCourse(APIView):
    def get(self, request, fid):
        course = Course.objects.filter(faculty=fid)
        serializer = FetchCourseSerializer(course, many=True)
        print(serializer.data)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class AddCourse(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        collegeId = request.user.id
        course = CourceDetail.objects.filter(college=collegeId)
        # if course.count()>0:
        serilize = CourceDetailInsertSerializer(course, many=True)
        return Response(serilize.data)
        # else:
        #     return Response({'message':1})

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def post(self, request):
        data = OrderedDict()
        data.update(request.data)
        cource = request.data['course']
        collegeId = request.user.id
        data['college'] = collegeId
        college = College.objects.get(id=collegeId)
        serializer = CourceDetailInsertSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if not college.add_course:
                college.add_course = True
                college.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=422)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        data = OrderedDict()
        data.update(request.data)
        collegeId = request.user.id
        data['college'] = collegeId
        getcourse = CourceDetail.objects.get(college=collegeId, id=data['id'])
        serializer = CourseDetailEditSerializer(getcourse, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=409)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def delete(self, request):
        cid = request.user.id
        course = CourceDetail.objects.get(id=request.GET.get('id'), college=cid)
        course.delete()
        return Response({'message': "delete success"}, status=202)


@permission_classes((permissions.AllowAny,))
class CollegeCourceListAPI(APIView):
    def get(self, request, cid, fid):
        course = CourceDetail.objects.filter(college=cid, faculty=fid).values_list('course', flat=True).distinct()
        cname = Course.objects.filter(id__in=list(course)).values('id', 'name')
        print(list(cname))
        return Response({'course': list(cname)})
        # return Response({'message':1})


@permission_classes((permissions.AllowAny,))
class CourseDetailApi(APIView):
    def get(self, request, cid, courceId):
        try:
            course = CourceDetail.objects.get(college=uuid.UUID(cid), id=courceId)
            serializer = CourceDetailInsertSerializer(course)
            courcedata = serializer.data
            return Response(courcedata)
        except CourceDetail.DoesNotExist:
            return Response({'error': 'doesnt exist'}, status=404)
        # return Response({'message':1})

#
# @permission_classes((permissions.AllowAny,))
# class DocumentApi(APIView):
#     def get(self, request):
#         documentlist = MinimumDoc.objects.all()
#         if len(documentlist) > 0:
#             serializer = MinimumDocSerializer(documentlist, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({'message': 'empty'}, status=204)
#

@permission_classes((permissions.AllowAny,))
class FacilityAPI(APIView):
    def get(self, request):
        facilitylist = Facility.objects.all()
        if len(facilitylist) > 0:
            serializer = FacilitySerializer(facilitylist, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'empty'}, status=204)


@permission_classes((permissions.AllowAny,))
class AddFacilityApi(APIView):
    def post(self, request):
        try:
            id = request.data['id']
            for i in request.data['facility']:
                facility = Facility.objects.get(id=i)
                college = College.objects.get(id=id)
                college.facility.add(facility)

            return Response({'message': 'success'}, status=200)
        except Facility.DoesNotExist:
            return Response({'message': 'facility id is not match'}, status=404)
        except College.DoesNotExist:
            return Response({'message': 'college id is not match'}, status=404)


@permission_classes((permissions.AllowAny,))
class CollegeDetailAPI(APIView):
    def get(self, request):
        bookmark = False
        applyed = False
        id = uuid.UUID(request.GET.get('cid'))
        # b41aa823-e41b-4ec1-902d-b8548ebb1162
        college = College.objects.get(id=id)
        course = CourceDetail.objects.filter(college=id)
        gallary = Gallery.objects.filter(college=id)
        facility = college.facility.all()
        serializer = CollegeSerializer(college)
        serializercourse = CourceDetailInsertSerializer(course, many=True)
        serializerfacility = FacilitySerializer(facility, many=True)
        serializerGallery = CollegeGallertStudentpage(gallary, many=True)
        col = serializer.data
        col['course'] = serializercourse.data
        col['facility'] = serializerfacility.data
        col['gallary'] = serializerGallery.data
        if request.GET.get('sid'):
            sid = uuid.UUID(request.GET.get('sid'))
            visited = VisitedCollege.objects.filter(college=id, student=sid).exists()
            applyfind = StudentApply.objects.filter(college=id, student=sid).exists()
            bookmarkfind = Bookmark.objects.filter(college=id, student=sid).exists()
            if bookmarkfind:
                bookmark = True
            if applyfind:
                applyed = True
            if not visited:
                serializervisit = CollegeVisitSerializer(data={'college': id, 'student': sid})
                if serializervisit.is_valid():
                    serializervisit.save()
                else:
                    return Response(serializervisit.errors, status=422)
        col.update({'applyed': applyed, "bookmark": bookmark})
        return Response(col)


@permission_classes((permissions.AllowAny,))
class GallaryAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        # id=uuid.UUID('83831bbf-3c4c-4b1f-bba0-4db75d00485f')
        id = request.user.id
        findgallery = Gallery.objects.filter(college=id)
        if findgallery is not None:
            serializer = GallerySerializer(findgallery, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': None}, status=404)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def post(self, request):
        data = request.data
        data._mutable = True
        data['college'] = request.user.id
        serializer = GallerySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=401)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        try:
            data = OrderedDict()
            data.update(request.data)
            id = data['id']
            data['college'] = request.user.id
            findgallery = Gallery.objects.get(id=id, college=request.user.id)
            update_serializer = GallerySerializer(findgallery, data=data)
            if update_serializer.is_valid():
                update_serializer.save()
                return Response(update_serializer.data)
            else:
                return Response(update_serializer.errors)
        except Gallery.DoesNotExist:
            return Response({'message': 'id is not match'}, status=400)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def delete(self, request):
        try:
            college = request.user.id
            pic = Gallery.objects.get(id=request.GET.get('id'), college=college)
            pic.delete()
            return Response({'message': "delete successs"})
        except Gallery.DoesNotExist:
            return Response({'message': 'id is not match'}, status=400)


@permission_classes((permissions.AllowAny,))
class StatisticsApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        cid = request.user.id
        enddate = datetime.datetime.now()
        day = request.GET.get('day')
        data = application_report_count(cid, day)
        return Response(data)


@permission_classes((permissions.AllowAny,))
class ChartApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        id = request.user.id
        date = request.GET.get('day')
        if date == 'week':
            data = date_wise_filter(id)
        elif date == "today":
            data = application_report_count(id, '1')
        elif date == "month":
            year = request.GET.get('year')
            print(id)
            # accept=StudentApply.objects.filter(college=id,status=0,apply_date__year="2021",apply_date__month=5).count()
            # print(accept)
            data = count_yeardata(id, year)
            return Response(data)
        else:
            return Response({"message": 1})
        return Response(data)


@permission_classes((permissions.AllowAny,))
class StudentApplication(APIView, NotificationMixin):
    notification_group = ['portal_user']
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        id = request.user.id
        find = StudentApply.objects.filter(college=id, status__in=['0', '1', '2', '3'],
                                           student_action__in=['1', '2', '3'])
        print(find)
        if find is not None:
            serializer = StudentStatusSerializer(find, many=True)
            return Response(serializer.data)
        return Response({"message": None})
        # return Response({"message":1})

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        try:
            sid, id, status = uuid.UUID(request.data['student']), request.data['id'], request.data['status']
            if status in ['1', '2', '3']:
                action_date = datetime.datetime.now()
                getdata = StudentApply.objects.get(id=id, student=sid, college=request.user.id)
                serializer = UpdateStatusSeializer(getdata, data={'status': status, 'action_date': action_date})
                if serializer.is_valid():
                    serializer.save()
                    # send notification
                    data = {
                        'name': 'Application Status Changed',
                        'image': getdata.college.logourl.url,
                        'content': 'Application Status Changed',
                        'id': str(getdata.college.id)
                    }
                    self.send_notification(data=data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
            else:
                return Response({'message': "status not found"}, status=303)
        except StudentApply.DoesNotExist:
            return Response({'message': "status not found"}, status=404)


@permission_classes((permissions.AllowAny,))
class CommentApplication(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def post(self, request):
        data = request.data  # application id and message
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        aid = request.GET.get('id')  # application id
        comment = Comment.objects.filter(apply=aid)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def delete(self, request):
        commentid = request.GET.get('id')  # comment id
        comment = Comment.objects.get(id=commentid)
        comment.delete()
        return Response({"message": "comment delete successfully"})

        # serializer=


@permission_classes((permissions.AllowAny,))
class EnrolledStudentApi(APIView, NotificationMixin):
    notification_group = ['portal_user']
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        id = request.user.id
        find = StudentApply.objects.filter(college=id, student_action='4')
        print(find)
        if find is not None:
            serializer = StudentStatusSerializer(find, many=True)
            return Response(serializer.data)
        return Response({"message": None})

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        try:
            sid, id, enrolled = uuid.UUID(request.data['student']), request.data['id'], request.data['enrolled']
            # if status in ['4','5']:
            action_date = datetime.datetime.now()
            getdata = StudentApply.objects.get(id=id, student=sid, college=request.user.id)
            serializer = UpdateStatusSeializer(getdata, data={'enrolled': enrolled, 'action_date': action_date})
            if serializer.is_valid():
                serializer.save()
                # send notification
                data = {
                    'name': 'Student Enrolled',
                    'image': getdata.college.logourl.url,
                    'content': 'Application Status Changed',
                    'id': str(getdata.college.id)
                }
                self.send_notification(data=data)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
            # else:
            #     return Response({'message':"status not found"},status=303)
        except StudentApply.DoesNotExist:
            return Response({'message': "status not found"}, status=404)


@permission_classes((permissions.AllowAny,))
class ViewedStudentDetails(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        try:
            college = request.user.id
            sid = uuid.UUID(request.GET.get('sid'))
            id = request.GET.get('id')
            apply = StudentApply.objects.get(id=id, student=sid, college=college)
            serializer = StudentApplySerializer(apply).data
            if serializer['view'] == False:
                data = StudentApply.objects.filter(id=id).update(view=True, view_date=datetime.datetime.now())
                studentdata = get_student_detail(sid)
                return Response(studentdata)
            else:
                studentdata = get_student_detail(sid)
                return Response(studentdata)

        except StudentApply.DoesNotExist:
            return Response({'message': "status not found"}, status=404)


@permission_classes((permissions.AllowAny,))
class NotAcceptableCountry(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        cid = request.user.id
        # cid=uuid.UUID('4c547fb3-d768-4bfa-98f3-db2acece43c7')
        country = RestrictCountry.objects.filter(cid=cid)
        serializer = GetCountryRestrictedSerializer(country, many=True)
        return Response(serializer.data)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def post(self, request):
        listofcountry = request.data['country']
        cid = request.user.id
        # cid=uuid.UUID('4c547fb3-d768-4bfa-98f3-db2acece43c7')
        if len(listofcountry) > 0:
            listdata = []
            converter = lambda id, country: listdata.append({'cid': id, 'country': country})
            for i in listofcountry:
                converter(cid, i)
            print(listdata)
            college = College.objects.get(id=cid)
            serializer = RestrictCountrySerializer(data=listdata, many=True)
            if serializer.is_valid():
                serializer.save()
                if not college.select_restricted_country:
                    college.select_restricted_country = True
                    college.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=409)
        else:
            return Response({'message': 0})

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def delete(self, request):
        cid = request.user.id
        id = request.GET.get('id')
        country = RestrictCountry.objects.get(id=id, cid=cid)
        country.delete()
        return Response({'message': 'data delate success'})


@permission_classes((permissions.AllowAny,))
class LocationAPI(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        cid = request.user.id
        data = OrderedDict()
        data.update(request.data)
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(data['lat'] + "," + data['long'])
        data['location'] = str(location)
        college = College.objects.get(id=cid)
        serializer = LocationSerializer(college, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=422)


class StaffApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def post(self, request):
        return Response({'message': 'this is staff api'})


@permission_classes((permissions.AllowAny,))
class FormOpen(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        data = OrderedDict()
        data.update(request.data)
        cid = request.user.id
        id = data['id']
        course = CourceDetail.objects.get(college=cid, id=id)
        serialize = CourceDetailFormSerializer(course, data=data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        else:
            return Response(serialize.errors)


@permission_classes((permissions.AllowAny,))
class CounselorAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def post(self, request):
        data = OrderedDict()
        data.update(request.data)
        cid = request.user.id
        data['college'] = cid
        print(data)
        serializer = CouncilorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=409)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        cid = request.user.id
        counselor_id = request.GET.get('counselor_id')
        if counselor_id is None:
            councilor = CounselorModel.objects.filter(college=cid)
            serializer = CouncilorSerializer(councilor, many=True)
            return Response(serializer.data)
        else:
            councilor = CounselorModel.objects.get(college=cid, id=counselor_id)
            serializer = CouncilorSerializer(councilor)
            return Response(serializer.data)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        data = OrderedDict()
        data.update(request.data)
        cid = request.user.id
        data['college'] = cid
        councilor_id = request.GET.get("councilor_id")
        councilor = CounselorModel.objects.get(college=cid, id=councilor_id)
        serializer = CouncilorSerializer(councilor, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def delete(self, request):
        cid = request.user.id
        councilor_id = request.GET.get("councilor_id")
        councilor = CounselorModel.objects.get(college=cid, id=councilor_id)
        councilor.delete()
        return Response({"message": "delete councilor success"})


@permission_classes((permissions.AllowAny,))
class AccomodationApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def post(self, request):
        data = OrderedDict()
        data.update(request.data)
        cid = request.user.id
        data['college'] = cid

        serializer = AccomodationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=409)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        cid = request.user.id
        aid = request.GET.get('aid')
        if aid is None:
            accomodation = Accomodation.objects.filter(college=cid)
            serializer = AccomodationSerializer(accomodation, many=True)
            return Response(serializer.data)
        else:
            try:
                accomodation = Accomodation.objects.get(college=cid, id=aid)
                serializer = AccomodationSerializer(accomodation)
                return Response(serializer.data)
            except Accomodation.DoesNotExist:
                return Response({"message": "accomodation doesnt exist", "status": False})

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        data = OrderedDict()
        data.update(request.data)
        cid = request.user.id
        aid = request.GET.get('id')
        data.update({"college": cid})
        find = Accomodation.objects.get(id=aid, college=cid)
        update = AccomodationSerializer(find, data=data)
        if update.is_valid():
            update.save()
            return Response(update.data)
        else:
            return Response(update.errors)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def delete(self, request):
        cid = request.user.id
        aid = request.GET.get('id')
        accomodation = Accomodation.objects.get(college=cid, id=aid)
        accomodation.delete()
        return Response({"message": "accomodation data delete successfully"})


@permission_classes((permissions.AllowAny,))
class CanteenApi(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def post(self, request):
        data = OrderedDict()
        data.update(request.data)
        cid = request.user.id
        data['college'] = cid
        print(data)
        serializer = CanteenSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=409)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        try:
            cid = request.user.id
            print("cansdgjasdh", cid)
            # cid=uuid.UUID('4c547fb3-d768-4bfa-98f3-db2acece43c7')
            data = Canteen.objects.get(college=cid)
            serializer = CanteenSerializer(data)
            print(serializer.data)
            return Response(serializer.data)
        except Canteen.DoesNotExist:
            return Response({'message': 'doesnt exist', 'status': False})

    permissions_classes = [IsAuthenticated]

    @method_decorator([college_required], name="dispatch")
    def put(self, request):
        data = OrderedDict()
        data.update(request.data)
        cid = request.user.id
        college = Canteen.objects.get(college=cid)
        data['college'] = cid
        update = CanteenSerializer(college, data=data)
        if update.is_valid():
            update.save()
            return Response(update.data)
        else:
            return Response(update.errors)
    # permissions_classes = [IsAuthenticated]
    # @method_decorator([ college_required],name="dispatch")
    # def delete(self,request):
    #     cid=request.user.id
    #     college=College.objects.get(id=cid)
    #     college.de


@permission_classes((permissions.AllowAny,))
class LaboratoryApi(APIView):
    def get(self, request):
        try:
            lid = request.GET.get('id')
            cid = request.user.id
            if lid == None:
                lab = Laboratory.objects.filter(college=cid)
                serializer = LaboratorySerializer(lab, many=True)
                return Response(serializer.data)
            else:
                lab = Laboratory.objects.get(college=cid, id=lid)
                serializer = LaboratorySerializer(lab)
                return Response(serializer.data)
        except Laboratory.DoesNotExist:
            return Response({"message": "doesnt exist", "status": False})

    def post(self, request):
        data = OrderedDict()
        data.update(request.data)
        cid = request.user.id
        data.update({'college': cid})
        serializer = LaboratorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def put(self, request):
        try:
            data = OrderedDict()
            data.update(request.data)
            cid = request.user.id
            lid = request.GET.get('id')
            data.update({'college': cid})
            find = Laboratory.objects.get(id=lid, college=cid)

            serializer = LaboratorySerializer(find, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

        except Laboratory.DoesNotExist:
            return Response({"message": "data doesnt exist", "status": False})

    def delete(self, request):
        try:
            cid = request.user.id
            lid = request.GET.get('id')
            lab = Laboratory.objects.get(id=lid, college=cid)
            lab.delete()
            return Response({"message": "lab data delete successfully"})
        except Laboratory.DoesNotExist:
            return Response({'message': "doesnt exist"})
    # def put(self , request)


@permission_classes((permissions.AllowAny,))
class Library(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        try:
            sid = request.user.id
            library = LibraryModel.objects.get(college=sid)
            serializer = LibrarySerializer(library)
            return Response(serializer.data)
        except LibraryModel.DoesNotExist:
            return Response({"message": "library doesnt exist", "status": False})

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def post(self, request):
        data = OrderedDict()
        data.update(request.data)
        data.update({"college": request.user.id})
        upload = request.GET.get('upload')
        if upload is None:
            serializer = LibrarySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=409)
        else:
            return Response({"message": "1"})

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def put(self, request):
        data = OrderedDict()
        data.update(request.data)
        sid = request.user.id
        data.update({"college": sid})
        library = LibraryModel.objects.get(college=sid)
        serializer = LibrarySerializer(library, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def delete(self, request):
        sid = request.user.id
        library = LibraryModel.objects.get(college=sid)
        library.delete()
        return Response({"message": "data delete successfully"})


@permission_classes((permissions.AllowAny,))
class BlogApi(APIView):
    def get(self, request):
        bid = request.GET.get('id')
        cid = request.user.id
        if bid is not None:
            blog = Blog.objects.find(college=cid)
            serializer = BlogSerializer(blog, many=True)
            return Response(serializer.data)
        else:
            blog = Blog.objects.get(college=cid, id=bid)
            serializer = BlogSerializer(blog)
            return Response(serializer.data)

    def post(self, request):
        return Response({"message": "this is post"})

    def put(self, request):
        return Response({"message": "this is put"})

    def delete(self, request):
        return Response({"message": "this is delete"})
