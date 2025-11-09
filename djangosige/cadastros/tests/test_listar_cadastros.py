from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestAcessoViewListarCadastros(TestCase):
    """Testar o acesso a página de listagem dos cadastros"""

    def test_o_usuario_que_nao_estiver_logado_nao_acessa_pagina_de_listagem_dos_cadastros(self):
        """o usuário que não estiver logado não acessa a página de listagem dos cadastros"""
        request = self.client.get(reverse("cadastros:listar"))
        self.assertEqual(request.status_code, 302)

    def test_url_que_o_usuario_nao_autenticado_e_redirecionado_quando_tentar_acessar_pagina_de_listagem_dos_cadastros(
        self,
    ):
        """a URL que o usuario nao autenticado é redirecionado quando tentar acessar a página de listagem dos cadastros"""
        request = self.client.get(reverse("cadastros:listar"))
        self.assertRedirects(request, "/login/")


class TestContextoViewListarCadastros(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="johndoe", password="john@doe.123")

    def setUp(self):
        self.client.force_login(self.user)
        self.request = self.client.get(reverse("cadastros:listar"))

    def test_o_usuario_logado_pode_acessar_pagina_de_listagem_dos_cadastros(self):
        """o usuario logado pode acessar a página de listagem dos cadastros"""
        self.assertEqual(self.request.status_code, 200)

    def test_o_nome_template_usado_para_renderizar_pagina_de_listagem_dos_cadastros(self):
        """o nome do template usado para renderizar a página de listagem dos cadastros"""
        self.assertTemplateUsed(self.request, "cadastros/listar.html")

    def test_palavra_chave_pagina_esta_no_contexto_da_resposta_da_listagem_de_cadastros(self):
        """a palavra chave "pagina" está no contexto da resposta da listagem de cadastros"""
        self.assertIn("pagina", self.request.context)

    def test_o_valor_da_palavra_chave_pagina_e_cadastros(self):
        """o valor da palavra chave "página" é "cadastros"."""
        self.assertEqual(self.request.context["pagina"], "cadastros")
