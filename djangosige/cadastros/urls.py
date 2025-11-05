from django.urls import path

from . import views

app_name = "cadastros"

urlpatterns = [
    path("", views.ListarCadastros.as_view(), name="listar_cadastros"),
    path(
        "r/<str:relacionamento>/",
        views.ListarCadastros.as_view(),
        name="listar_cadastros_por_relacionamento",
    ),
    path("criar/", views.CriarCadastro.as_view(), name="criar_cadastro"),
    path("<int:pk>/", views.VerCadastro.as_view(), name="ver_cadastro"),
    path("<int:pk>/editar/", views.EditarCadastro.as_view(), name="editar_cadastro"),
]
