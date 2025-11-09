from django import forms

from .models import Pessoa

FormularioCriarPessoa = forms.modelform_factory(
    Pessoa,
    fields=(
        "descricao",
        "tipo_pessoa",
        "e_cliente",
        "e_fornecedor",
        "e_transportadora",
        "observacoes",
    ),
)


FormularioEditarPessoa = forms.modelform_factory(
    Pessoa,
    fields=(
        "descricao",
        "tipo_pessoa",
        "e_cliente",
        "e_fornecedor",
        "e_transportadora",
        "observacoes",
        "esta_ativo",
    ),
)
