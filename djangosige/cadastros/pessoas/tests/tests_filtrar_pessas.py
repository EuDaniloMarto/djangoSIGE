from django.test import TestCase

from ..filters import FiltrarPessoa
from ..models import Pessoa
from .factories import PessoaFactory


class TestFiltrarPessoa(TestCase):
    def test_filtro_por_descricao_usa_icontains(self):
        filtro = FiltrarPessoa(data={"descricao": "abc"})
        lookup = filtro.filters["descricao"].lookup_expr
        self.assertEqual(lookup, "icontains")

    def test_queryset_filtra_corretamente(self):
        PessoaFactory.create(descricao="Cliente XPTO")
        PessoaFactory.create(descricao="Fornecedor Beta")

        filtro = FiltrarPessoa(
            data={"descricao": "cliente"}, queryset=Pessoa.objects.all()
        )
        result = filtro.qs
        self.assertEqual(result.count(), 1)
        self.assertIn("Cliente XPTO", [p.descricao for p in result])
        self.assertIn("Cliente XPTO", [p.descricao for p in result])
