import django_filters

from .models import Pessoa


class FiltrarPessoa(django_filters.FilterSet):
    descricao = django_filters.CharFilter(
        field_name="descricao", lookup_expr="icontains", label=""
    )

    class Meta:
        model = Pessoa
        fields = ["descricao"]
