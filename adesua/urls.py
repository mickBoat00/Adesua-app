from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("apps.course.urls", namespace="course")),
    path("api/", include("apps.ratings.urls", namespace="ratings")),
    path("api/search/", include("apps.search.urls")),
    path("api/", include("apps.reviewers.urls")),
    path("api/enrollment/", include("apps.enrollment.urls", namespace="enrollment")),
    path("api/promotion/", include("apps.promotion.urls", namespace="promotion")),
    path("api/profile/", include("apps.profiles.urls")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("docs/", include_docs_urls(title="AdesuaAPI")),
    path(
        "schema",
        get_schema_view(title="Adesua API", description="API for the Adesua Platform Backend..", version="1.0.0"),
        name="openapi-schema",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Adesua Admin"
admin.site.site_title = "Adesua Admin Portal"
admin.site.index_title = "Adesua Admin"
