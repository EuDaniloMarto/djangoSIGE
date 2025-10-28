from django.urls import path

from . import views

app_name = "cadastros"

urlpatterns = [
    path("", views.ListarCadastros.as_view(), name="listar_cadastros"),
    path("<int:pk>/", views.VerCadastro.as_view(), name="ver_cadastro"),
]
