from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.credenciais = {
            "username": "teste",
            "password": "test1234",
        }
        UserModel.objects.create_user(**self.credenciais)

    def test_codigo_status_ok_quando_usuario_esta_autenticado(self):
        self.client.login(**self.credenciais)
        self.assertEqual(
            self.client.get(reverse("dashboard_index")).status_code, HTTPStatus.OK
        )

    def test_codigo_status_found_quando_usuario_nao_autenticado(self):
        self.assertEqual(
            self.client.get(reverse("dashboard_index")).status_code, HTTPStatus.FOUND
        )

    def test_nome_template_usado_renderizar_resposta(self):
        self.client.login(**self.credenciais)
        self.assertTemplateUsed(
            self.client.get(reverse("dashboard_index")),
            "dashboard/dashboard_index.html",
        )

    def test_chave_data_atual_esta_no_contexto_da_resposta(self):
        self.client.login(**self.credenciais)
        self.assertIn("data_atual", self.client.get(reverse("dashboard_index")).context)

    def test_chave_quantidade_cadastro_esta_no_contexto_da_resposta(self):
        self.client.login(**self.credenciais)
        self.assertIn(
            "quantidade_cadastro", self.client.get(reverse("dashboard_index")).context
        )

    def test_chave_agenda_hoje_esta_no_contexto_da_resposta(self):
        self.client.login(**self.credenciais)
        self.assertIn(
            "agenda_hoje", self.client.get(reverse("dashboard_index")).context
        )

    def test_chave_alertas_esta_no_contexto_da_resposta(self):
        self.client.login(**self.credenciais)
        self.assertIn("alertas", self.client.get(reverse("dashboard_index")).context)
