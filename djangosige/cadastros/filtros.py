import django_filters as filters

from .models import Pessoa


class FiltroPessoa(filters.FilterSet):
    descricao = filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = Pessoa
        fields = ["descricao"]
