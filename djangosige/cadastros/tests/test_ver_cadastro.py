from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve

from djangosige.cadastros.pessoas.models import Pessoa
from djangosige.cadastros.pessoas.tests.factories import PessoaFactory
from djangosige.cadastros.views import VerCadastro


class TestUrlVerCadastro(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pessoa = PessoaFactory.create()

    def setUp(self):
        self.resolver = resolve(self.pessoa.get_absolute_url())

    def test_a_URL_deve_resolver_para_a_classe_de_view_correta(self):
        self.assertEqual(self.resolver.func.view_class, VerCadastro)

    def test_o_nome_da_URL_deve_ser_ver_cadastro(self):
        self.assertEqual(self.resolver.url_name, "ver_cadastro")

    def test_o_namespace_deve_ser_cadastros(self):
        self.assertEqual(self.resolver.app_name, "cadastros")

    def test_a_rota_da_URL_deve_ser_n_cadastros_pk(self):
        self.assertEqual(self.resolver.route, "n/cadastros/<int:pk>/")


class TestAcessoVerCadastro(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.pessoa = PessoaFactory.create(colaborador=cls.user)

    def test_o_usuario_nao_autenticado_deve_receber_codigo_de_redirecionamento(self):
        response = self.client.get(self.pessoa.get_absolute_url())
        self.assertEqual(response.status_code, 302)

    def test_o_usuario_nao_autenticado_deve_ser_redirecionado_para_a_tela_de_login(
        self,
    ):
        response = self.client.get(self.pessoa.get_absolute_url())
        self.assertIn("/login/", response.url)

    def test_a_view_deve_retornar_HTTP_200_para_usuarios_autenticados(self):
        self.client.force_login(self.user)
        response = self.client.get(self.pessoa.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_view_deve_retornar_404_se_o_usuario_tentar_acessar_um_cadastro_que_nao_existe(
        self,
    ):
        self.client.force_login(self.user)
        response = self.client.get("/n/cadastros/9999/")
        self.assertEqual(response.status_code, 404)


class TestContextoVerCadastro(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.pessoa = PessoaFactory.create(colaborador=cls.user)

    def setUp(self):
        self.client.force_login(self.user)
        self.response = self.client.get(self.pessoa.get_absolute_url())

    def test_o_nome_do_template_usado(self):
        self.assertTemplateUsed(self.response, "cadastros/ver_cadastro.html")

    def test_a_palavra_chave_pagina_deve_estar_no_contexto(self):
        self.assertIn("pagina", self.response.context)

    def test_o_valor_da_palavra_chave_pagina_eh_cadastro(self):
        self.assertEqual(self.response.context["pagina"], "cadastros")

    def test_a_palavra_chave_cadastro_deve_estar_no_contexto(self):
        self.assertIn("cadastro", self.response.context)

    def test_o_cadastro_no_contexto_deve_ser_uma_instancia_de_Pessoa(self):
        self.assertIsInstance(self.response.context["cadastro"], Pessoa)

    def test_o_cadastro_no_contexto_deve_corresponder_ao_pk_da_URL(self):
        self.assertEqual(self.response.context["cadastro"].pk, self.pessoa.pk)
