from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/courses/', include('apps.course.urls')),
    path('api/doc/', include_docs_urls(title='AdesuaAPI')),
    path('schema', get_schema_view(
        title="Adesua API",
        description="API for the Adesua Platform Backend..",
        version="1.0.0"
    ), name='openapi-schema'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
