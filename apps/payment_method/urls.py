from django.urls import path

from apps.payment_method import views

urlpatterns = [
    path(
        '<institute_id>/provider/add',
        views.AddProviderPaymentMethod.as_view(),
        name="add_provider"
    ),
    path(
        '<provider_payment_id>/provider/update',
        views.UpdateProviderPaymentMethod.as_view(),
        name="update-provider"
    ),
    path(
        '<voucher_id>/voucher/update',
        views.UpdateVoucherPaymentMethod.as_view(),
        name="update_voucher"
    ),
    path(
        '<voucher_id>/voucher/delete',
        views.DeleteVoucherPaymentMethod.as_view(),
        name="delete-voucher"
    ),
    path(
        '<provider_id>/provider/delete',
        views.DeleteProviderPaymentMethod.as_view(),
        name="delete-provider"
    ),
    path(
        '<institute_id>/voucher/add',
        views.AddVoucherPaymentDetail.as_view(),
        name="voucher-add"
    ),
    path(
        '<institute_id>/voucher/list',
        views.ListVoucherPaymentView.as_view(),
        name="list-voucher"
    ),
    path(
        '<institute_id>/provider/list',
        views.ListProviderPaymentMethod.as_view(),
        name = "provider-list"
    ),
    path(
        'list_provider_name',
        views.ListProviderName.as_view(),
        name='list-provider-name'
    )

]