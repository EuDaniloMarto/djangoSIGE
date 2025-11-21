import pytest

from ..forms import FormVerPessoa


@pytest.mark.django_db
def test_o_formulario_para_ver_um_cadastro_deve_conter_os_seguintes_campos():
    """O formulário para editar um cadastro deve conter os seguintes campos."""
    form = FormVerPessoa()
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
