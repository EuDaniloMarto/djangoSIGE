from django.urls import path

from . import views

app_name = "djangosige"

urlpatterns = [
    path("", views.PaginaInicial.as_view(), name="pagina_inicial"),
]
