from django import forms

from .models import Pessoa


class FormCriarPessoa(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = [
            "descricao",
            "tipo_pessoa",
            "e_cliente",
            "e_fornecedor",
            "e_transportadora",
            "observacoes",
        ]


class FormEditarPessoa(FormCriarPessoa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.fields["tipo_pessoa"]
        field.widget.attrs["readonly"] = "readonly"

    class Meta(FormCriarPessoa.Meta):
        model = Pessoa
        fields = [
            "descricao",
            "tipo_pessoa",
            "e_cliente",
            "e_fornecedor",
            "e_transportadora",
            "esta_ativo",
            "observacoes",
        ]


class FormVerPessoa(FormEditarPessoa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs["disabled"] = "disabled"
