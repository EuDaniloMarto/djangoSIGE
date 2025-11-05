from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from djangosige.cadastros.pessoas.models import Pessoa
from djangosige.cadastros.views import CriarCadastro


class TestUrlCriarCadastros(TestCase):
    def setUp(self):
        self.resolver = resolve(reverse("cadastros:criar_cadastro"))

    def test_a_URL_deve_resolver_para_a_classe_de_view_correta(self):
        self.assertEqual(self.resolver.func.view_class, CriarCadastro)

    def test_o_nome_da_URL_deve_ser_criar_cadastro(self):
        self.assertEqual(self.resolver.url_name, "criar_cadastro")

    def test_o_namespace_deve_ser_cadastros(self):
        self.assertEqual(self.resolver.app_name, "cadastros")

    def test_a_rota_da_URL_quando_criar_cadastro(self):
        self.assertEqual(self.resolver.route, "n/cadastros/criar/")


class TestAcessoCriarCadastros(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.url = reverse("cadastros:criar_cadastro")

    def test_o_usuario_nao_autenticado_deve_receber_codigo_de_redirecionamento(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_o_usuario_nao_autenticado_deve_ser_redirecionado_para_a_tela_de_login(
        self,
    ):
        response = self.client.get(self.url)
        self.assertIn("/login/", response.url)

    def test_a_view_deve_retornar_HTTP_200_para_usuarios_autenticados(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestContextoCriarCadastro(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.url = reverse("cadastros:criar_cadastro")

    def setUp(self):
        self.client.force_login(self.user)
        self.request = self.client.get(self.url)

    def test_o_nome_do_template_usado(self):
        self.assertTemplateUsed(self.request, "cadastros/criar_cadastro.html")

    def test_a_palavra_chave_pagina_deve_estar_no_contexto(self):
        self.assertIn("pagina", self.request.context)

    def test_o_valor_da_palavra_chave_pagina_eh_cadastro(self):
        self.assertEqual(self.request.context["pagina"], "cadastros")


class TestFormularioCriarCadastros(TestCase):
    def test_o_form_class_deve_ser_uma_ModelForm_de_Pessoa(self):
        form_class = CriarCadastro.form_class
        self.assertTrue(issubclass(form_class, forms.ModelForm))

    def test_os_campos_do_form_devem_ser_os_definidos_na_view(self):
        expected_fields = [
            "descricao",
            "tipo_pessoa",
            "eh_cliente",
            "eh_fornecedor",
            "eh_transportadora",
            "observacoes",
        ]
        form_class = CriarCadastro.form_class
        self.assertListEqual(list(form_class().fields), expected_fields)


class TestCriarCadastros(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.url = reverse("cadastros:criar_cadastro")

    def setUp(self):
        self.client.force_login(self.user)

    def test_um_cadastro_eh_realizado_com_sucesso(self):
        data = {
            "descricao": "Cliente XPTO",
            "tipo_pessoa": "PJ",
            "eh_cliente": True,
            "eh_fornecedor": False,
            "eh_transportadora": False,
            "observacoes": "Teste",
        }
        self.client.post(reverse("cadastros:criar_cadastro"), data)
        self.assertEqual(Pessoa.objects.count(), 1)


class TestCriarCadastrosFormularioInvalido(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.url = reverse("cadastros:criar_cadastro")

    def setUp(self):
        self.data_invalida = {
            "descricao": "",
            "tipo_pessoa": "PJ",
            "eh_cliente": False,
            "eh_fornecedor": False,
            "eh_transportadora": False,
            "observacoes": "",
        }

    def test_status_code_quando_form_invalido_deve_ser_200(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.data_invalida)
        self.assertEqual(response.status_code, 200)

    def test_template_usado_quando_form_invalido(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.data_invalida)
        self.assertTemplateUsed(response, "cadastros/criar_cadastro.html")

    def test_objeto_nao_deve_ser_criado_quando_form_invalido(self):
        self.client.force_login(self.user)
        self.client.post(self.url, self.data_invalida)
        self.assertEqual(Pessoa.objects.count(), 0)
