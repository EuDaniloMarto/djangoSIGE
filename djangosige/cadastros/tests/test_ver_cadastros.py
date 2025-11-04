from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestListarCadastros(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credenciais = {"username": "johndoe", "password": "john@doe.test"}
        get_user_model().objects.create_user(**cls.credenciais)
        return super().setUpTestData()

    def test_usuario_nao_esta_logado(self):
        request = self.client.get(reverse("cadastros:ver_cadastros", kwargs={"pk": 1}))
        self.assertEqual(request.status_code, 302)

    def test_usuario_esta_logado(self):
        self.client.login(**self.credenciais)
        request = self.client.get(reverse("cadastros:ver_cadastros", kwargs={"pk": 1}))
        self.assertEqual(request.status_code, 200)

    def test_nome_template_usado(self):
        self.client.login(**self.credenciais)
        request = self.client.get(reverse("cadastros:ver_cadastros", kwargs={"pk": 1}))
        self.assertTemplateUsed(request, "cadastros/ver_cadastros.html")
