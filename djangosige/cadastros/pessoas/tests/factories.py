import factory
from factory import fuzzy

from djangosige.tests.factories import UserFactory

from ..models import Pessoa


class PessoaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pessoa

    colaborador = factory.SubFactory(UserFactory)
    descricao = fuzzy.FuzzyText()
    tipo_pessoa = fuzzy.FuzzyChoice(choices=Pessoa.EscolherTipoPessoa.values)
    eh_cliente = fuzzy.FuzzyChoice(choices=[True, False])
    eh_fornecedor = fuzzy.FuzzyChoice(choices=[True, False])
    eh_transportadora = fuzzy.FuzzyChoice(choices=[True, False])
    ativo = fuzzy.FuzzyChoice(choices=[True, False])
    observacoes = fuzzy.FuzzyText()
