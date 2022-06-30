from django.shortcuts import render

from apps.consultancy.mixins import ConsultancyMixin
from apps.consultancy_course.mixins import ConsultancyCourseMixin
from apps.core import generics
# Create your views here.
class AddConsultancyCourse(generics.CreateAPIView,ConsultancyMixin):
    pass

class ListConsultancyCourse(generics.ListAPIView,ConsultancyMixin):
    pass

class UpdateConsultancyCourse(generics.UpdateAPIView,ConsultancyCourseMixin):
    pass

class DeleteConsultancyCourse(generics.DestroyWithMessageAPIView,ConsultancyCourseMixin):
    pass