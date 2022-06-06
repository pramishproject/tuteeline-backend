from django.contrib import admin

# Register your models here.
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from apps.geo_location.models import Hotel


@admin.register(Hotel)
class HotelAdmin(LeafletGeoAdmin):
    list_display = ("id", "name", "address", "location", "created_at", "updated_at")
