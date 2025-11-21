import pytest

from ..forms import FormCriarPessoa
from ..models import Pessoa


@pytest.mark.django_db
def test_o_formulario_para_criar_um_cadastro_deve_conter_os_seguintes_campos_na_ordem():
    """O formulário para criar um cadastro deve conter os seguintes campos."""
    form = FormCriarPessoa()
    expected_fields = [
        "descricao",
        "tipo_pessoa",
        "e_cliente",
        "e_fornecedor",
        "e_transportadora",
        "observacoes",
    ]
    assert list(form.fields.keys()) == expected_fields


@pytest.mark.django_db
def test_o_formulario_para_criar_um_cadastro_deve_ser_valido_quando_todos_os_dados_fornecidos_estao_corretos():
    """O formulário para criar um cadastro deve ser válido quando todos os dados fornecidos estão corretos."""

    form = FormCriarPessoa(
        data={
            "descricao": "Marina Cristiane Dias",
            "tipo_pessoa": Pessoa.EscolherTipoPessoa.PF,
            "e_cliente": True,
            "e_fornecedor": False,
            "e_transportadora": False,
            "observacoes": "",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_o_formulario_para_criar_um_cadastro_deve_ser_invalido_quando_a_descricao_nao_for_fornecido():
    """O formulário para a criar um cadastro deve ser inválido quando a descrição não for fornecida."""

    form = FormCriarPessoa(
        data={
            "tipo_pessoa": Pessoa.EscolherTipoPessoa.PF,
            "e_cliente": True,
            "e_fornecedor": False,
            "e_transportadora": False,
            "observacoes": "",
        }
    )

    assert not form.is_valid()


@pytest.mark.django_db
def test_o_formulario_para_criar_um_cadastro_deve_ser_invalido_quando_a_descricao_for_vazia():
    """O formulário para a criar um cadastro deve ser inválido quando a descrição for vazia."""

    form = FormCriarPessoa(
        data={
            "descricao": "",
            "tipo_pessoa": Pessoa.EscolherTipoPessoa.PF,
            "e_cliente": True,
            "e_fornecedor": False,
            "e_transportadora": False,
            "observacoes": "",
        }
    )

    assert not form.is_valid()
