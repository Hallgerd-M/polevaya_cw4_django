from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("messaging/admin/", admin.site.urls),
    path("messaging/", include("message_sending.urls", namespace="messaging")),
    path("users/", include("users.urls", namespace="users")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
