from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Cadastro


class ListarCadastros(LoginRequiredMixin, ListView):
    model = Cadastro
    template_name = "cadastros/listar_cadastros.html"
    paginate_by = 10
    context_object_name = "cadastros"


class VerCadastro(LoginRequiredMixin, DetailView):
    model = Cadastro
    template_name = "cadastros/ver_cadastro.html"
    context_object_name = "cadastro"
