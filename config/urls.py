"""Configurações das URLs do projeto djangosige"""

from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("djangosige.apps.base.urls")),
    path("login/", include("djangosige.apps.login.urls")),
    path("cadastro/", include("djangosige.apps.cadastro.urls")),
    path("fiscal/", include("djangosige.apps.fiscal.urls")),
    path("vendas/", include("djangosige.apps.vendas.urls")),
    path("compras/", include("djangosige.apps.compras.urls")),
    path("financeiro/", include("djangosige.apps.financeiro.urls")),
    path("estoque/", include("djangosige.apps.estoque.urls")),
]

if settings.DEBUG:
    urlpatterns = [
        *urlpatterns,
        *static(settings.MEDIA_URL, documento_root=settings.MEDIA_ROOT),
    ]
