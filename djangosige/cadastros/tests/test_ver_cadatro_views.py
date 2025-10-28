from django.contrib.auth import get_user_model
from django.test import TestCase

from .factories import CadastroFactory


class TestUsuarioNaoEstaLogado(TestCase):
    """O usuário não está logado"""

    def test_status_code_eh_302(self):
        cadastro = CadastroFactory()
        request = self.client.get(cadastro.get_absolute_url())
        self.assertEqual(request.status_code, 302)


class TestUsuarioEstaLogado(TestCase):
    """O usuário está logado"""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="usertest", password="passtest"
        )
        return super().setUpTestData()

    def test_status_code_eh_200(self):
        self.client.login(username="usertest", password="passtest")
        cadastro = CadastroFactory()
        request = self.client.get(cadastro.get_absolute_url())
        self.assertEqual(request.status_code, 200)

    def test_nome_do_objeto_do_context_eh_cadastro(self):
        self.client.login(username="usertest", password="passtest")
        cadastro = CadastroFactory()
        request = self.client.get(cadastro.get_absolute_url())
        self.assertIn("cadastro", request.context)
