import pytest

from ..forms import FormEditarPessoa
from ..models import Pessoa
from .factories import PessoaFactory


@pytest.fixture
def pessoa():
    return PessoaFactory(
        descricao="Bryan Victor Benício Sales",
        tipo_pessoa=Pessoa.EscolherTipoPessoa.PF,
        e_cliente=True,
        e_fornecedor=False,
        e_transportadora=False,
        esta_ativo=True,
    )


@pytest.mark.django_db
def test_o_formulario_para_editar_um_cadastro_deve_conter_os_seguintes_campos():
    """O formulário para editar um cadastro deve conter os seguintes campos."""
    form = FormEditarPessoa()
    expected_fields = [
        "descricao",
        "tipo_pessoa",
        "e_cliente",
        "e_fornecedor",
        "e_transportadora",
        "esta_ativo",
        "observacoes",
    ]
    assert list(form.fields.keys()) == expected_fields


@pytest.mark.django_db
def test_o_formulario_para_editar_um_cadastro_deve_ser_valido_quando_todos_os_dados_fornecidos_estao_corretos(pessoa):
    """O formulário para editar um cadastro deve ser válido quando todos os dados fornecidos estão corretos."""

    form = FormEditarPessoa(
        data={
            "descricao": "Marina Cristiane Dias",
            "tipo_pessoa": Pessoa.EscolherTipoPessoa.PF,
            "e_cliente": True,
            "e_fornecedor": False,
            "e_transportadora": False,
            "observacoes": "lorem ipsum dolor sit amet.",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_o_formulario_para_editar_um_cadastro_deve_ser_invalido_quando_a_descricao_nao_for_fornecido(pessoa):
    """O formulário para a editar um cadastro deve ser inválido quando a descrição não for fornecida."""

    form = FormEditarPessoa(
        data={
            "tipo_pessoa": Pessoa.EscolherTipoPessoa.PF,
            "e_cliente": True,
            "e_fornecedor": False,
            "e_transportadora": False,
            "observacoes": "",
        },
        instance=pessoa,
    )

    assert not form.is_valid()


@pytest.mark.django_db
def test_o_formulario_para_editar_um_cadastro_deve_ser_invalido_quando_a_descricao_for_vazia(pessoa):
    """O formulário para a editar um cadastro deve ser inválido quando a descrição for vazia."""

    form = FormEditarPessoa(
        data={
            "descricao": "",
            "tipo_pessoa": Pessoa.EscolherTipoPessoa.PF,
            "e_cliente": True,
            "e_fornecedor": False,
            "e_transportadora": False,
            "observacoes": "",
        },
        instance=pessoa,
    )

    assert not form.is_valid()
