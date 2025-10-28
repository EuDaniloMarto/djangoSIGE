from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ListarCadastros(LoginRequiredMixin, TemplateView):
    template_name = "cadastros/listar_cadastros.html"
