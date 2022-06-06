from django.urls import path
from apps.geo_location.views import HotelUpdateRetreiveView, ListCreateGenericViews

urlpatterns = [
    path("hotels", ListCreateGenericViews.as_view()),
    path(
        "hotels/<str:pk>",
        HotelUpdateRetreiveView.as_view(),
    ),
]