from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ListarCadastros(LoginRequiredMixin, TemplateView):
    extra_context = {"pagina": "cadastros"}
    template_name = "cadastros/listar.html"
