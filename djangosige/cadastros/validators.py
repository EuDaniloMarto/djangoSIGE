import brutils as br
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_cpf(value):
    if not value:
        return value

    cpf_numero = br.remove_symbols_cep(value)
    if br.is_valid_cpf(cpf_numero):
        return cpf_numero

    raise ValidationError(_("Número de CPF inválido."))


def validate_cnpj(value):
    if not value:
        return value

    cnpj_numero = br.remove_symbols_cnpj(value)
    if br.is_valid_cnpj(cnpj_numero):
        return cnpj_numero

    raise ValidationError(_("Número de CNPJ inválido."))


def validate_telefone(value):
    if not value:
        return

    apenas_digitos = br.remove_symbols_phone(value)

    if not br.is_valid_phone(apenas_digitos):
        raise ValidationError(_("O telefone é inválido"))
