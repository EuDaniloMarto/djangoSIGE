import pytest
from brutils import format_cnpj, format_cpf, generate_cnpj, generate_cpf
from django.core.exceptions import ValidationError

from djangosige.cadastros.validators import validate_cnpj, validate_cpf


def test_o_validador_de_cpf_deve_aceitar_strings_vazias():
    """O validador de CPF deve aceitar strings vazias"""

    assert validate_cpf("") == ""


def test_o_validador_de_cpf_deve_aceitar_cpfs_validos_sem_formatacao():
    """O validador de CPF deve aceitar CPFs válidos sem formatação"""

    cpf = generate_cpf()
    assert validate_cpf(cpf) == cpf


def test_o_validador_de_cpf_deve_aceitar_cpfs_validos_com_formatacao():
    """O validador de CPF deve aceitar CPFs válidos com formatação"""

    cpf = generate_cpf()
    assert validate_cpf(format_cpf(cpf)) == cpf


def test_o_validador_de_cpf_deve_rejeitar_cpfs_com_menos_de_11_digitos():
    """O validador de CPF deve rejeitar CPFs com menos de 11 dígitos"""

    with pytest.raises(ValidationError) as e:
        validate_cpf(generate_cpf()[:9])
    assert "Número de CPF inválido." in str(e.value)


def test_o_validador_de_cpf_deve_rejeitar_cpfs_com_mais_de_11_digitos():
    """O validador de CPF deve rejeitar CPFs com mais de 11 dígitos"""

    with pytest.raises(ValidationError) as e:
        validate_cpf(generate_cpf() + "12")
    assert "Número de CPF inválido." in str(e.value)


@pytest.mark.parametrize(
    "cpf",
    [
        "00000000000",
        "11111111111",
        "22222222222",
        "33333333333",
        "44444444444",
        "55555555555",
        "66666666666",
        "77777777777",
        "88888888888",
        "99999999999",
    ],
)
def test_o_validador_de_cpf_deve_rejeitar_cpfs_cujos_digitos_sao_todos_iguais(cpf):
    """O validador de CPF deve rejeitar CPFs cujos dígitos são todos sequenciais"""

    with pytest.raises(ValidationError) as e:
        validate_cpf(cpf)
    assert "Número de CPF inválido." in str(e.value)


def test_o_validador_de_cpf_deve_rejeitar_cpfs_invalidos():
    """O validador de CPF deve rejeitar CPFs inválidos"""

    with pytest.raises(ValidationError) as e:
        validate_cpf("12345678910")
    assert "Número de CPF inválido." in str(e.value)


def test_o_validador_de_cpf_deve_rejeitar_cpfs_com_caracteres_nao_numericos():
    """O validador de CPF deve rejeitar CPFs que contenham caracteres não-numéricos (letras, etc.)"""

    with pytest.raises(ValidationError) as e:
        validate_cpf("123.456.789-XX")
    assert "Número de CPF inválido." in str(e.value)


def test_o_validador_de_cnpj_deve_aceitar_strings_vazias():
    """O validador de CNPJ deve aceitar strings vazias"""

    assert validate_cnpj("") == ""


def test_o_validador_de_cnpj_deve_aceitar_cnpjs_validos_sem_formatacao():
    """O validador de CNPJ deve aceitar CNPJs válidos sem formatação"""

    cnpj = generate_cnpj()
    assert validate_cnpj(cnpj) == cnpj


def test_o_validador_de_cnpj_deve_aceitar_cnpjs_validos_com_formatacao():
    """O validador de CNPJ deve aceitar CNPJs válidos com formatação"""

    cnpj = generate_cnpj()
    assert validate_cnpj(format_cnpj(cnpj)) == cnpj


def test_o_validador_de_cnpj_deve_rejeitar_cnpjs_com_menos_de_14_digitos():
    """O validador de CNPJ deve rejeitar CNPJs com menos de 14 dígitos"""

    with pytest.raises(ValidationError) as e:
        validate_cnpj(generate_cnpj()[:10])
    assert "Número de CNPJ inválido." in str(e.value)


def test_o_validador_de_cnpj_deve_rejeitar_cnpjs_com_mais_de_14_digitos():
    """O validador de CNPJ deve rejeitar CNPJs com mais de 14 dígitos"""

    with pytest.raises(ValidationError) as e:
        validate_cnpj(generate_cnpj() + "123")
    assert "Número de CNPJ inválido." in str(e.value)


@pytest.mark.parametrize(
    "cnpj",
    [
        "00000000000000",
        "11111111111111",
        "22222222222222",
        "33333333333333",
        "44444444444444",
        "55555555555555",
        "66666666666666",
        "77777777777777",
        "88888888888888",
        "99999999999999",
    ],
)
def test_o_validador_de_cnpj_deve_rejeitar_cnpjs_cujos_digitos_sao_todos_iguais(cnpj):
    """O validador de CNPJ deve rejeitar CNPJs cujos dígitos são todos iguais"""

    with pytest.raises(ValidationError) as e:
        validate_cnpj(cnpj)
    assert "Número de CNPJ inválido." in str(e.value)


def test_o_validador_de_cnpj_deve_rejeitar_cnpjs_invalidos_pela_matematica():
    """O validador de CNPJ deve rejeitar CNPJs inválidos pelos dígitos verificadores"""

    with pytest.raises(ValidationError) as e:
        validate_cnpj("12345678901234")
    assert "Número de CNPJ inválido." in str(e.value)


def test_o_validador_de_cnpj_deve_rejeitar_cnpjs_com_caracteres_nao_numericos():
    """O validador de CNPJ deve rejeitar CNPJs que contenham caracteres não-numéricos (letras, etc.)"""

    with pytest.raises(ValidationError) as e:
        validate_cnpj("12.345.678/9012-AA")
    assert "Número de CNPJ inválido." in str(e.value)
