from django.contrib import admin

from .models import College, Faculty
from .models import Course, Facility, CourceDetail, RestrictCountry, Laboratory, Canteen, Accomodation, StanderedRating


admin.site.register((College, Course, Facility, CourceDetail, Faculty, RestrictCountry, Laboratory, Canteen,
                     Accomodation, StanderedRating))
