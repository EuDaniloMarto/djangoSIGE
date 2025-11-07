from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView

from djangosige.cadastros.pessoas.models import Pessoa
from djangosige.cadastros.pessoas.filters import FiltrarPessoa
# >>>
# CREATE
# <<<


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


# >>>
# READ
# <<<


class ListarCadastros(LoginRequiredMixin, FilterView):
    extra_context = {"pagina": "cadastros"}
    model = Pessoa
    template_name = "cadastros/listar_cadastros.html"
    context_object_name = "cadastros"
    paginate_by = 25
    filterset_class = FiltrarPessoa

    def get_relacionamento(self):
        relacionamento = self.kwargs.get("relacionamento")
        return (
            relacionamento
            if relacionamento in {"cliente", "fornecedor", "transportadora"}
            else None
        )

    def get_queryset(self):
        queryset = super().get_queryset()

        relacionamento = self.get_relacionamento()
        if relacionamento:
            queryset = queryset.filter(**{f"eh_{relacionamento}": True})

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


# >>>
# UPDATE
# <<<


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


# >>>
# DELETE
# <<<
