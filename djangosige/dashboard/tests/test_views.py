from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class TestCaseDashboardView(TestCase):
    def setUp(self):
        self.credenciais = {
            "username": "john_doe",
            "password": "johndoe123",
        }
        UserModel.objects.create_user(**self.credenciais)

    def test_usuario_autenticado_pode_acessar_pagina_dashboard(self):
        self.client.login(**self.credenciais)
        response = self.client.get(reverse("dashboard_index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_usuario_nao_atenticado_nao_pode_acessar_pagina_dashboard(self):
        response = self.client.get(reverse("dashboard_index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_atributo_data_atual_esta_na_resposta_da_view_dashboard(self):
        self.client.login(**self.credenciais)
        response = self.client.get(reverse("dashboard_index"))
        self.assertIn("data_atual", response.context)

    def test_atributo_quantidade_cadastro_esta_na_resposta_da_view_dashboard(self):
        self.client.login(**self.credenciais)
        response = self.client.get(reverse("dashboard_index"))
        self.assertIn("quantidade_cadastro", response.context)

    def test_atributo_agenda_hoje_esta_na_resposta_da_view_dashboard(self):
        self.client.login(**self.credenciais)
        response = self.client.get(reverse("dashboard_index"))
        self.assertIn("agenda_hoje", response.context)

    def test_atributo_alertas_esta_na_resposta_da_view_dashboard(self):
        self.client.login(**self.credenciais)
        response = self.client.get(reverse("dashboard_index"))
        self.assertIn("alertas", response.context)
