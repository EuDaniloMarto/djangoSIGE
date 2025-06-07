"""Configurações das URLs do projeto djangosige"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("djangosige.base.urls")),
    path("login/", include("djangosige.login.urls")),
    path("cadastro/", include("djangosige.cadastro.urls")),
    path("fiscal/", include("djangosige.fiscal.urls")),
    path("vendas/", include("djangosige.vendas.urls")),
    path("compras/", include("djangosige.compras.urls")),
    path("financeiro/", include("djangosige.financeiro.urls")),
    path("estoque/", include("djangosige.estoque.urls")),
]

if settings.DEBUG:
    urlpatterns = [
        *urlpatterns,
        *static(settings.MEDIA_URL, documento_root=settings.MEDIA_ROOT),
    ]
