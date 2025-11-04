from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CriarCadastros(LoginRequiredMixin, TemplateView):
    template_name = "cadastros/criar_cadastros.html"


class ListarCadastros(LoginRequiredMixin, TemplateView):
    template_name = "cadastros/listar_cadastros.html"


class VerCadastros(LoginRequiredMixin, TemplateView):
    template_name = "cadastros/ver_cadastros.html"


class EditarCadastros(LoginRequiredMixin, TemplateView):
    template_name = "cadastros/editar_cadastros.html"
