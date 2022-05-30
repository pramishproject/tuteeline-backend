import datetime
from datetime import timedelta

from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.college.models import College
from apps.college.serializers import CollegeCardSerializer, StudentStatusSerializer
from apps.core.decorators import college_required
from apps.student.models import StudentApply


@permission_classes((permissions.AllowAny,))
class SearchCollege(APIView):
    def get(self, request):
        query = request.GET.get('q', None)
        page = request.GET.get('page', None)
        print(query)
        if query is not None:
            college_reasult = College.objects.search(query)
            print(college_reasult)
            if len(college_reasult):
                pegination = Paginator(college_reasult, 18)
                pagelist = pegination.page(page).object_list
                serializer = CollegeCardSerializer(pagelist, many=True)
                return Response(serializer.data)
        return Response({"message": "query is null"}, status=404)


@permission_classes((permissions.AllowAny,))
class SearchListApi(APIView):
    def get(self, request):
        query = request.GET.get('query', None)
        if query is not None:
            college_reasult = College.objects.search(query)[0:10]
            college_name = college_reasult.values_list('name', flat=True)
            return Response({'name': list(college_name)})

        return Response({"message": 1})


@permission_classes((permissions.AllowAny,))
class SearchApplicationForm(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator([college_required], name='dispatch')
    def get(self, request):
        name = request.GET.get('name', None)
        time = request.GET.get('time', None)
        course = request.GET.get('course', None)
        college = request.user.id

        if name is not None and name.strip() and time is not None and time.strip() and course is not None and course.strip():
            now = datetime.date.today()
            if time == "day":
                now = datetime.date.today()
                application = StudentApply.objects.filter(
                    college=college, apply_date__contains=now,
                    course__icontains=course, first_name__icontains=name)
            elif time == "week":
                day = now - timedelta(days=7)
                application = StudentApply.objects.filter(college=college, apply_date__lte=day,
                                                          course__icontains=course, first_name__icontains=name)
            elif time == "Month":
                year = now.year
                month = now.month
                application = StudentApply.objects.filter(college=college, apply_date__year=year,
                                                          apply_date__month=month, course__icontains=course,
                                                          first_name__icontains=name)
            serialize = StudentStatusSerializer(application, many=True)
            return Response(serialize.data)
        elif name is not None and name.strip() and not time.strip() and not course.strip():
            application = StudentApply.objects.filter(first_name__icontains=name, college=college)
            serialize = StudentStatusSerializer(application, many=True)
            return Response(serialize.data)
        elif course.strip() and not name.strip() and not time.strip():
            application = StudentApply.objects.filter(course__icontains=course)
            serialize = StudentStatusSerializer(application, many=True)
            return Response(serialize.data)
        elif time.strip() and not name.strip() and not course.strip():
            now = datetime.date.today()
            if time == "day":
                now = datetime.date.today()
                application = StudentApply.objects.filter(college=college, apply_date__contains=now)
            elif time == "week":
                day = now - timedelta(days=7)
                application = StudentApply.objects.filter(college=college, apply_date__lte=day)
            elif time == "Month":
                year = now.year
                month = now.month
                application = StudentApply.objects.filter(college=college, apply_date__year=year,
                                                          apply_date__month=month)

        elif time.strip() and name.strip() and not course.strip():
            now = datetime.date.today()
            if time == "day":
                now = datetime.date.today()
                application = StudentApply.objects.filter(college=college, apply_date__contains=now,
                                                          first_name__icontains=name)
            elif time == "week":
                day = now - timedelta(days=7)
                application = StudentApply.objects.filter(college=college, apply_date__lte=day,
                                                          first_name__icontains=name)
            elif time == "Month":
                year = now.year
                month = now.month
                application = StudentApply.objects.filter(college=college, apply_date__year=year,
                                                          apply_date__month=month, first_name__icontains=name)
            serialize = StudentStatusSerializer(application, many=True)
            return Response(serialize.data)
        elif time.strip() and course.strip() and not name.strip():
            now = datetime.date.today()
            if time == "day":
                now = datetime.date.today()
                application = StudentApply.objects.filter(college=college, apply_date__contains=now,
                                                          course__icontains=course)
            elif time == "week":
                day = now - timedelta(days=7)
                application = StudentApply.objects.filter(college=college, apply_date__lte=day,
                                                          course__icontains=course, )
            elif time == "Month":
                year = now.year
                month = now.month
                application = StudentApply.objects.filter(college=college, apply_date__year=year,
                                                          apply_date__month=month, course__icontains=course)
            serialize = StudentStatusSerializer(application, many=True)
            return Response(serialize.data)
        elif course.strip() and name.strip() and not time.strip():
            application = StudentApply.objects.filter(course__icontains=course, first_name__icontains=name)
            serialize = StudentStatusSerializer(application, many=True)
            return Response(serialize.data)

        return Response({'message': "not found"}, status=404)
