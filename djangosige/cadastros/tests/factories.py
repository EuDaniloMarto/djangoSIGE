import factory
from django.contrib.auth import get_user_model
from factory import fuzzy

from ..choices import EscolherBanco
from ..models import Banco, Documento, Email, Endereco, Pessoa, Site, Telefone

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fuzzy.FuzzyText()
    password = fuzzy.FuzzyText()


class PessoaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pessoa

    colaborador = factory.SubFactory(UserFactory)
    descricao = fuzzy.FuzzyText()
    tipo_pessoa = fuzzy.FuzzyChoice(Pessoa.EscolherTipoPessoa.values)
    e_cliente = fuzzy.FuzzyChoice([True, False])
    e_fornecedor = fuzzy.FuzzyChoice([True, False])
    e_transportadora = fuzzy.FuzzyChoice([True, False])
    esta_ativo = fuzzy.FuzzyChoice([True, False])
    observacoes = fuzzy.FuzzyText()


class EnderecoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Endereco

    pessoa = factory.SubFactory(PessoaFactory)
    e_principal = fuzzy.FuzzyChoice([True, False])
    logradouro = fuzzy.FuzzyText()
    numero = fuzzy.FuzzyInteger(low=0, high=9999)
    complemento = fuzzy.FuzzyText()
    bairro = fuzzy.FuzzyText()
    municipio = fuzzy.FuzzyText()
    uf = fuzzy.FuzzyText()
    pais = fuzzy.FuzzyText()
    cep = fuzzy.FuzzyInteger(low=11111111, high=99999999)
    e_entrega = fuzzy.FuzzyChoice([True, False])
    e_cobranca = fuzzy.FuzzyChoice([True, False])


class TelefoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Telefone

    pessoa = factory.SubFactory(PessoaFactory)
    e_principal = fuzzy.FuzzyChoice([True, False])
    telefone = fuzzy.FuzzyInteger(low=11111111111, high=99999999999)


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Email

    pessoa = factory.SubFactory(PessoaFactory)
    e_principal = fuzzy.FuzzyChoice([True, False])
    email = f"{fuzzy.FuzzyText()}@mail.com"


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site

    # Herdado de RegistroPrincipalPorPessoa
    pessoa = factory.SubFactory(PessoaFactory)
    e_principal = fuzzy.FuzzyChoice([True, False])
    site = f"www.{fuzzy.FuzzyText()}.com"


class BancoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Banco

    pessoa = factory.SubFactory(PessoaFactory)
    e_principal = fuzzy.FuzzyChoice([True, False])

    banco = fuzzy.FuzzyChoice(EscolherBanco.values)
    agencia = fuzzy.FuzzyInteger(low=1111, high=99999)
    conta = fuzzy.FuzzyInteger(low=1111, high=99999)
    digito = fuzzy.FuzzyInteger(low=0, high=9)


class DocumentoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Documento

    pessoa = factory.SubFactory(PessoaFactory)
    e_principal = fuzzy.FuzzyChoice([True, False])
    documento = fuzzy.FuzzyText(length=200)
