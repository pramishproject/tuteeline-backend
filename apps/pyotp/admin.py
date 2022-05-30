from django.contrib import admin

from apps.pyotp.models import PyOTP


@admin.register(PyOTP)
class PyOTPAdmin(admin.ModelAdmin):
    """
    """
    list_display = (
        'id',
        'user',
        'interval',
        'otp',
        'expires_at',
    )
    list_display_links = ('user',)
    search_fields = (
        'otp',
    )
    list_per_page = 20
    ordering = ('-created_at',)
