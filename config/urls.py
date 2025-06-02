""""Configurações das URLs do projeto DjangoSIGE"""


from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("djangosige.urls")),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
