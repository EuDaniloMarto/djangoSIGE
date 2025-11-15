import django_filters as filters
from django import forms
from django.forms import TypedChoiceField

from .models import Pessoa

BOOLEAN_CHOICES = (
    ("", "------------"),  # <-- Opção vazia / Placeholder
    ("1", "Sim"),  # O valor aqui deve ser o que o filtro espera para True
    ("0", "Não"),  # O valor aqui deve ser o que o filtro espera para False
)


class FiltroPessoa(filters.FilterSet):
    descricao = filters.CharFilter(
        lookup_expr="icontains",
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Diga-me quem você está buscando...",
            }
        ),
    )
    e_cliente = filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        empty_label=None,  # Define choices diretamente, não precisamos de empty_label
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    e_fornecedor = filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    e_transportadora = filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    esta_ativo = filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Pessoa
        fields = [
            "descricao",
            "tipo_pessoa",
            "e_cliente",
            "e_fornecedor",
            "e_transportadora",
            "esta_ativo",
        ]
