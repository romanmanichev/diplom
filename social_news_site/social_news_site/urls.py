from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from . import settings
from articles.views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('articles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found