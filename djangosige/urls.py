from django.urls import include, path

urlpatterns = [
    path("", include("djangosige.base.urls")),
    path("login/", include("djangosige.login.urls")),
    path("cadastro/", include("djangosige.cadastro.urls")),
    path("fiscal/", include("djangosige.fiscal.urls")),
    path("vendas/", include("djangosige.vendas.urls")),
    path("compras/", include("djangosige.compras.urls")),
    path("financeiro/", include("djangosige.financeiro.urls")),
    path("estoque/", include("djangosige.estoque.urls")),
]
