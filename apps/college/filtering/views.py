from django.db.models import Q
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.college.models import CourceDetail, College
from apps.college.serializers import CollegeCardSerializer


@permission_classes((permissions.AllowAny,))
class CollegeFilteringApi(APIView):
    def get(self, request):
        country = request.GET.get('country', None)
        max_fee = request.GET.get('max_fee', None)
        min_fee = request.GET.get('min_fee', None)
        min_review = request.GET.get('min_review', None)
        max_review = request.GET.get('max_review', None)
        eligibility = request.GET.get('eligibility', None)
        scholorship = request.GET.get('scholorship', None)
        print("scholorship", type(scholorship))
        course = request.GET.get('course', None)
        duration = request.GET.get('duration', None)
        types = request.GET.get('type', None)
        country_query = Q()
        fee_query = Q()
        eligibility_query = Q()
        type_query = Q()
        scholor_query = Q()
        course_query = Q()
        cour_query = Q()
        if country is not None and country.strip():
            # country=country.split(',')
            print("*)))))))))))", country)
            # country_query=Q(country__ignorecase__in=country)
            country_query = Q(country=country)

        if max_fee and min_fee is not None and min_fee.strip() and max_fee.strip():
            min_fee = int(min_fee)
            max_fee = int(max_fee)
            fee_query = Q(fee__range=(min_fee, max_fee))

        if eligibility is not None and eligibility.strip():
            # eligibilitylst=eligibility.split(',')
            # eligibility_query=Q(eligibility_exam__in=eligibilitylst)
            eligibility_query = Q(eligibility_exam__icontains=eligibility)

        if scholorship is not None and scholorship.strip():
            if scholorship == "1":
                print("**************************************************************************8")
                scholorship = True
                scholor_query = Q(schlorship=scholorship)
            elif scholorship == "0":
                scholorship = False
                scholor_query = Q(schlorship=scholorship)
            else:
                scholor_query = Q()

        if types is not None and types.strip():
            # types_list=types.split(',')
            # type_query=Q(type__in=types_list)
            collegetype = types
            type_query = Q(type__icontains=collegetype)

        if course is not None and course.strip():
            course_list = course.split(',')
            print(course_list)
            course_query = Q(course__in=course_list)
        cour = CourceDetail.objects.filter(eligibility_query, fee_query)
        if cour is not None:
            cour_query = Q(courcedetail__in=cour)
        col = College.objects.filter(scholor_query, country_query, type_query, cour_query).distinct()
        serializers = CollegeCardSerializer(col, many=True)

        return Response(serializers.data)
