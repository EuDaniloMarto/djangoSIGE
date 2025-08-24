from django.urls import path, include
from django.conf import settings

from . import views


urlpatterns = [
    path("login/", include("djangosige.apps.login.urls")),
    path("cadastro/", include("djangosige.apps.cadastro.urls")),
    path("fiscal/", include("djangosige.apps.fiscal.urls")),
    path("vendas/", include("djangosige.apps.vendas.urls")),
    path("compras/", include("djangosige.apps.compras.urls")),
    path("financeiro/", include("djangosige.apps.financeiro.urls")),
    path("estoque/", include("djangosige.apps.estoque.urls")),
    path("", views.pagina_inicial, name="djangosige_pagina_inicial"),
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", views.handler404),
        path("500/", views.handler500),
    ]
