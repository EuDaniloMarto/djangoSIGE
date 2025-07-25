from django.urls import path, include
from . import views


urlpatterns = [
    path("", include("djangosige.base.urls")),
    path("login/", include("djangosige.login.urls")),
    path("cadastro/", include("djangosige.cadastro.urls")),
    path("fiscal/", include("djangosige.fiscal.urls")),
    path("vendas/", include("djangosige.vendas.urls")),
    path("compras/", include("djangosige.compras.urls")),
    path("financeiro/", include("djangosige.financeiro.urls")),
    path("estoque/", include("djangosige.estoque.urls")),
    path(
        "dev/",
        include(
            [
                path("", views.HomeView.as_view(), name="home"),
            ]
        )
    ),
]
