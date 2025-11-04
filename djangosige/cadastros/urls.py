from django.urls import path

from . import views

app_name = "cadastros"

urlpatterns = [
    path("", views.ListarCadastros.as_view(), name="listar_cadastros"),
    path("criar/", views.CriarCadastros.as_view(), name="criar_cadastros"),
    path("<int:pk>/", views.VerCadastros.as_view(), name="ver_cadastros"),
    path("<int:pk>/", views.EditarCadastros.as_view(), name="editar_cadastros"),
]
