from django.urls import path

from apps.payment_method import views

urlpatterns = [
    path(
        '<institute_id>/add',
        views.AddProviderPaymentMethod.as_view(),
        name="add_provider"
    )
]