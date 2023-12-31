from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from django.contrib import admin
from django.views import defaults as default_views
from kamiair.libs.rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='KAMI Airlines API')


urlpatterns = [
    path("", schema_view, name="list_api"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/", include('kamiair.apps.apis.urls', 
                    namespace='apis')),
    path("api-auth/", include('rest_framework.urls', 
                    namespace='api-auth')),
    ] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

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