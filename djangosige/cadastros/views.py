from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from djangosige.cadastros.pessoas.models import Pessoa


class CriarCadastro(LoginRequiredMixin, CreateView):
    extra_context = {"pagina": "cadastros"}
    template_name = "cadastros/criar_cadastro.html"
    form_class = forms.modelform_factory(
        Pessoa,
        fields=(
            "descricao",
            "tipo_pessoa",
            "eh_cliente",
            "eh_fornecedor",
            "eh_transportadora",
            "observacoes",
        ),
    )

    def form_valid(self, form):
        form.instance.colaborador = self.request.user
        return super().form_valid(form)


class ListarCadastros(LoginRequiredMixin, ListView):
    extra_context = {"pagina": "cadastros"}
    model = Pessoa
    template_name = "cadastros/listar_cadastros.html"
    context_object_name = "cadastros"

    def get_relacionamento(self):
        relacionamento = self.kwargs.get("relacionamento")
        lista_relacionamento = ("cliente", "fornecedor", "transportadora")
        return relacionamento if relacionamento in lista_relacionamento else None

    def get_queryset(self):
        relacionamento = self.get_relacionamento()
        queryset = Pessoa.objects.all()

        if relacionamento == "cliente":
            queryset = queryset.filter(eh_cliente=True)
        elif relacionamento == "fornecedor":
            queryset = queryset.filter(eh_fornecedor=True)
        elif relacionamento == "transportadora":
            queryset = queryset.filter(eh_transportadora=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("relacionamento", self.get_relacionamento())
        return context


class VerCadastro(LoginRequiredMixin, DetailView):
    extra_context = {"pagina": "cadastros"}
    template_name = "cadastros/ver_cadastro.html"
    model = Pessoa
    context_object_name = "cadastro"


class EditarCadastro(LoginRequiredMixin, UpdateView):
    extra_context = {"pagina": "cadastros"}
    template_name = "cadastros/editar_cadastro.html"
    form_class = forms.modelform_factory(
        Pessoa,
        fields=(
            "descricao",
            "tipo_pessoa",
            "eh_cliente",
            "eh_fornecedor",
            "eh_transportadora",
            "ativo",
            "observacoes",
        ),
    )
    model = Pessoa
    context_object_name = "cadastro"
