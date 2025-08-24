from http import HTTPStatus

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from unittest.mock import patch
from django.urls import reverse
from djangosige.views import handler404, handler500


UserModel = get_user_model()


class TestUsuarioTentaAcessarPaginaInicialSemAutenticacao(TestCase):
    def setUp(self):
        self.url = reverse("djangosige_pagina_inicial")
        return super().setUp()

    def test_codigo_status_found(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class TestUsuarioAutorizadoAcessaPaginaInicial(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.credenciais = {"username": "fulano", "password": "fulano@123"}
        cls.user = UserModel.objects.create_user(**cls.credenciais)

    def setUp(self):
        super().setUp()
        self.client.login(**self.credenciais)
        self.url = reverse("djangosige_pagina_inicial")

    def test_codigo_status_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_nome_template_usado(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "base/index.html")


class TestRespostaPaginaInicial(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.credenciais = {"username": "fulano", "password": "fulano@123"}
        cls.user = UserModel.objects.create_user(**cls.credenciais)

    def setUp(self):
        super().setUp()
        self.client.login(**self.credenciais)
        self.url = reverse("djangosige_pagina_inicial")

    def test_context_contains_quantidade_cadastro(self):
        response = self.client.get(self.url)
        self.assertIn("quantidade_cadastro", response.context)

    def test_context_contains_agenda_hoje(self):
        response = self.client.get(self.url)
        self.assertIn("agenda_hoje", response.context)

    def test_context_contains_alertas(self):
        response = self.client.get(self.url)
        self.assertIn("alertas", response.context)

    def test_context_contains_data_atual(self):
        response = self.client.get(self.url)
        self.assertIn("data_atual", response.context)

    def test_context_contains_movimento_caixa_keys(self):
        with patch(
            "djangosige.views.movimento_caixa",
            return_value={"saldo": 200, "movimento_caixa": 300},
        ):
            response = self.client.get(self.url)
            self.assertIn("saldo", response.context)
            self.assertIn("movimento_caixa", response.context)


class ErrorHandlersTestCase(TestCase):
    def test_handler404_returns_404(self):
        request = self.client.request().wsgi_request
        with patch("djangosige.views.render") as mock_render:
            handler404(request)
            mock_render.assert_called_with(request, "404.html", status=404)

    def test_handler500_returns_500(self):
        request = self.client.request().wsgi_request
        with patch("djangosige.views.render") as mock_render:
            handler500(request)
            mock_render.assert_called_with(request, "500.html", status=500)
