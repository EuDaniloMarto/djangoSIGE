from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django_filters.views import FilterView

from .filtros import FiltroPessoa
from .forms import FormCriarPessoa, FormEditarPessoa, FormVerPessoa
from .mixins import FilteredPaginationMixin, PaginaMixin
from .models import Pessoa


class ListarCadastros(LoginRequiredMixin, PaginaMixin, FilteredPaginationMixin, FilterView):
    template_name = "cadastros/listar.html"
    paginate_by = 25
    context_object_name = "cadastros"
    filterset_class = FiltroPessoa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["relacionamento"] = self.get_relacionamento()
        return context

    def get_ordering(self):
        return self.request.GET.get("ordering", "descricao")

    def get_queryset(self):
        queryset = Pessoa.objects.only(
            "pk", "descricao", "tipo_pessoa", "e_cliente", "e_fornecedor", "e_transportadora", "esta_ativo"
        )
        relacionamento = self.get_relacionamento()

        if relacionamento == "cliente":
            queryset = queryset.clientes()
        elif relacionamento == "fornecedor":
            queryset = queryset.fornecedores()
        elif relacionamento == "transportadora":
            queryset = queryset.transportadoras()
        else:
            queryset = queryset

        return queryset

    def get_relacionamento(self):
        relacionamento = self.request.GET.get("relacionamento")
        return relacionamento if relacionamento in ("cliente", "fornecedor", "transportadora") else None


class VerCadastro(LoginRequiredMixin, PaginaMixin, ModelFormMixin, DetailView):
    model = Pessoa
    template_name = "cadastros/ver.html"
    form_class = FormVerPessoa
    context_object_name = "cadastro"


class CriarCadastro(LoginRequiredMixin, PaginaMixin, CreateView):
    template_name = "cadastros/form.html"
    form_class = FormCriarPessoa

    def form_valid(self, form):
        form.instance.colaborador = self.request.user
        return super().form_valid(form)


class EditarCadastro(LoginRequiredMixin, PaginaMixin, UpdateView):
    model = Pessoa
    template_name = "cadastros/form.html"
    form_class = FormEditarPessoa
    context_object_name = "cadastro"
