from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestUsuarioNaoEstaLogado(TestCase):
    """O usuário não está logado"""

    def setUp(self):
        self.URL = reverse("cadastros:listar_cadastros")

    def test_status_code_eh_302(self):
        self.assertEqual(self.client.get(self.URL).status_code, 302)


class TestUsuarioEstaLogado(TestCase):
    """O usuário está logado"""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="usertest", password="passtest"
        )
        return super().setUpTestData()

    def setUp(self):
        self.URL = reverse("cadastros:listar_cadastros")

    def test_status_code_eh_200(self):
        self.client.login(username="usertest", password="passtest")
        self.assertEqual(self.client.get(self.URL).status_code, 200)
