import factory
from factory import fuzzy

from djangosige.tests.factories import UserFactory

from ..models import Cadastro


class CadastroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cadastro

    colaborador = factory.SubFactory(UserFactory)
    descricao = fuzzy.FuzzyText()
    tipo_cadastros = fuzzy.FuzzyChoice(Cadastro.TipoCadastro.values)
    eh_cliente = fuzzy.FuzzyChoice([True, False])
    eh_fornecedora = fuzzy.FuzzyChoice([True, False])
    eh_transportadora = fuzzy.FuzzyChoice([True, False])
    ativo = True
    observacoes = fuzzy.FuzzyText()
