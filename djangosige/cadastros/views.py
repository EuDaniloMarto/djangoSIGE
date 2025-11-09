from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import FormularioCriarPessoa, FormularioEditarPessoa
from .models import Pessoa


class ListarCadastros(LoginRequiredMixin, ListView):
    extra_context = {"pagina": "cadastros"}
    template_name = "cadastros/listar.html"
    queryset = Pessoa.objects.all()


class VerCadastro(LoginRequiredMixin, DetailView):
    extra_context = {"pagina": "cadastros"}
    template_name = "cadastros/listar.html"
    queryset = Pessoa.objects.all()


class CriarCadastro(LoginRequiredMixin, CreateView):
    extra_context = {"pagina": "cadastros"}
    template_name = "cadastros/listar.html"
    form_class = FormularioCriarPessoa

    def form_valid(self, form):
        self.form.instance.colaborador = self.request.user
        return super().form_valid()


class EditarCadastro(LoginRequiredMixin, UpdateView):
    extra_context = {"pagina": "cadastros"}
    template_name = "cadastros/listar.html"
    form_class = FormularioEditarPessoa
    queryset = Pessoa.objects.all()
