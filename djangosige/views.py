from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class PaginaInicial(LoginRequiredMixin, TemplateView):
    template_name = "djangosige/pagina_inicial.html"
