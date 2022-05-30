from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path(settings.ADMIN_URL, admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicons/favicon.ico'))),
    path(
        'notification/',
        include('apps.notification.urls')
    ),
]

if not settings.USE_S3:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

schema_view = get_schema_view(
    openapi.Info(
        title="Student Master API",
        default_version='v1',
        description="Student Master API",
    ),
)

# API URLS
urlpatterns += [
    path(
        'api/docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='api-docs'
    ),

    # api urls
    path(
        'v1/',
        include('config.api_urls')
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

admin.site.site_header = "Tutee Line"
admin.site.index_title = "Welcome to Student Master Admin Portal"
admin.site.site_title = "Student Master Admin Portal"
