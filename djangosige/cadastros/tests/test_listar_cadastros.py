from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from djangosige.cadastros.pessoas.models import Pessoa
from djangosige.cadastros.pessoas.tests.factories import PessoaFactory
from djangosige.cadastros.views import ListarCadastros


class TestUrlListarCadastros(TestCase):
    def setUp(self):
        self.resolver = resolve(reverse("cadastros:listar_cadastros"))

    def test_a_URL_deve_resolver_para_a_classe_de_view_correta(self):
        self.assertEqual(self.resolver.func.view_class, ListarCadastros)

    def test_o_nome_da_URL_deve_ser_listar_cadastros(self):
        self.assertEqual(self.resolver.url_name, "listar_cadastros")

    def test_o_namespace_deve_ser_cadastros(self):
        self.assertEqual(self.resolver.app_name, "cadastros")

    def test_a_rota_da_URL_quando_listar_todos_os_cadastros(self):
        self.assertEqual(self.resolver.route, "n/cadastros/")


class TestUrlListarCadastrosPorRelacionamento(TestCase):
    def setUp(self):
        self.resolver = resolve(
            reverse(
                "cadastros:listar_cadastros_por_relacionamento",
                kwargs={"relacionamento": "cliente"},
            )
        )

    def test_a_URL_deve_resolver_para_a_classe_de_view_correta(self):
        self.assertEqual(self.resolver.func.view_class, ListarCadastros)

    def test_o_nome_da_URL_deve_ser_listar_cadastros(self):
        self.assertEqual(self.resolver.url_name, "listar_cadastros_por_relacionamento")

    def test_o_namespace_deve_ser_cadastros(self):
        self.assertEqual(self.resolver.app_name, "cadastros")

    def test_a_rota_da_URL_quando_listar_os_cadastros_por_relacionamento(self):
        self.assertEqual(self.resolver.route, "n/cadastros/r/<str:relacionamento>/")


class TestAcessoListarCadastro(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.url = reverse("cadastros:listar_cadastros")

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


class TestAcessoListarCadastroPorRelacionamento(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.url = reverse(
            "cadastros:listar_cadastros_por_relacionamento",
            kwargs={"relacionamento": "cliente"},
        )

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


class TestContextoListarCadastros(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.url = reverse("cadastros:listar_cadastros")

    def setUp(self):
        self.client.force_login(self.user)
        self.request = self.client.get(self.url)

    def test_o_nome_do_template_usado(self):
        self.assertTemplateUsed(self.request, "cadastros/listar_cadastros.html")

    def test_a_palavra_chave_pagina_deve_estar_no_contexto(self):
        self.assertIn("pagina", self.request.context)

    def test_o_valor_da_palavra_chave_pagina_eh_cadastro(self):
        self.assertEqual(self.request.context["pagina"], "cadastros")

    def test_a_palavra_chave_cadastros_deve_estar_no_contexto(self):
        self.assertIn("cadastros", self.request.context)


class TestContextoListarCadastrosPorRelacionamento(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.url = reverse(
            "cadastros:listar_cadastros_por_relacionamento",
            kwargs={"relacionamento": "cliente"},
        )

    def setUp(self):
        self.client.force_login(self.user)
        self.request = self.client.get(self.url)

    def test_o_nome_do_template_usado(self):
        self.assertTemplateUsed(self.request, "cadastros/listar_cadastros.html")

    def test_a_palavra_chave_pagina_deve_estar_no_contexto(self):
        self.assertIn("pagina", self.request.context)

    def test_o_valor_da_palavra_chave_pagina_eh_cadastro(self):
        self.assertEqual(self.request.context["pagina"], "cadastros")

    def test_a_palavra_chave_cadastros_deve_estar_no_contexto(self):
        self.assertIn("cadastros", self.request.context)


class TestQuerySetListarCadastros(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )

    def setUp(self):
        self.client.force_login(self.user)
        PessoaFactory.create_batch(
            1,
            colaborador=self.user,
            eh_cliente=True,
            eh_fornecedor=True,
            eh_transportadora=True,
        )
        PessoaFactory.create_batch(
            1,
            colaborador=self.user,
            eh_cliente=True,
            eh_fornecedor=False,
            eh_transportadora=False,
        )
        PessoaFactory.create_batch(
            1,
            colaborador=self.user,
            eh_cliente=False,
            eh_fornecedor=True,
            eh_transportadora=False,
        )
        PessoaFactory.create_batch(
            1,
            colaborador=self.user,
            eh_cliente=False,
            eh_fornecedor=False,
            eh_transportadora=True,
        )

    def test_todos_os_objetos_da_query_deve_ser_uma_instancia_de_Pessoa(self):
        request = self.client.get(reverse("cadastros:listar_cadastros"))
        pessoas = request.context["cadastros"]
        self.assertTrue(all(isinstance(pessoa, Pessoa) for pessoa in pessoas))

    def test_todos_os_objetos_sao_listados(self):
        request = self.client.get(reverse("cadastros:listar_cadastros"))
        queryset = request.context["cadastros"]
        self.assertEqual(queryset.count(), 4)

    def test_lista_apenas_os_clientes(self):
        request = self.client.get(
            reverse(
                "cadastros:listar_cadastros_por_relacionamento",
                kwargs={"relacionamento": "cliente"},
            )
        )
        for pessoa in request.context["cadastros"]:
            self.assertTrue(pessoa.eh_cliente)

    def test_lista_apenas_os_fornecedores(self):
        request = self.client.get(
            reverse(
                "cadastros:listar_cadastros_por_relacionamento",
                kwargs={"relacionamento": "fornecedor"},
            )
        )
        for pessoa in request.context["cadastros"]:
            self.assertTrue(pessoa.eh_fornecedor)

    def test_lista_apenas_os_transportadoras(self):
        request = self.client.get(
            reverse(
                "cadastros:listar_cadastros_por_relacionamento",
                kwargs={"relacionamento": "transportadora"},
            )
        )
        for pessoa in request.context["cadastros"]:
            self.assertTrue(pessoa.eh_transportadora)

    def test_lista_todos_quando_relacionamento_invalido(self):
        response = self.client.get(
            reverse(
                "cadastros:listar_cadastros_por_relacionamento",
                kwargs={"relacionamento": "invalido"},
            )
        )
        queryset = response.context["cadastros"]
        self.assertEqual(queryset.count(), Pessoa.objects.count())


class TestMetodosGetQuerySetListarCadastros(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )

    def setUp(self):
        self.client.force_login(self.user)
        self.view = ListarCadastros()

    def test_o_metodo_get_relacionamento_deve_retornar_cliente_ou_fornecedor_ou_transportadora_para_os_respectivos_argumentos_na_URL(
        self,
    ):
        listar_relacionamentos = ("cliente", "fornecedor", "transportadora")

        for relacionamento in listar_relacionamentos:
            self.view.kwargs = {"relacionamento": relacionamento}
            self.assertIn(self.view.get_relacionamento(), listar_relacionamentos)

    def test_o_metodo_get_relacionamento_deve_retornar_None_se_o_argumento_na_URL_nao_for_cliente_ou_fornecedor_ou_transportadora(
        self,
    ):
        self.view.kwargs = {"relacionamento": "invalido"}
        self.assertIsNone(self.view.get_relacionamento())

    def test_o_metodo_get_relacionamento__deve_retornar_None_quando_nao_houver_argumento_na_URL(
        self,
    ):
        self.view.kwargs = {}
        self.assertIsNone(self.view.get_relacionamento())


class TestFiltroDescricao(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user", password="pass"
        )
        PessoaFactory(descricao="Cliente Alfa")
        PessoaFactory(descricao="Fornecedor Beta")
        PessoaFactory(descricao="Transportadora Gama")

    def setUp(self):
        self.client.force_login(self.user)
        self.url = reverse("cadastros:listar_cadastros")

    def test_filtro_retorna_apenas_itens_correspondentes(self):
        response = self.client.get(self.url, {"descricao": "cliente"})
        cadastros = response.context["cadastros"]
        self.assertEqual(cadastros.count(), 1)

    def test_filtro_sem_parametro_retorna_todos(self):
        response = self.client.get(self.url)
        cadastros = response.context["cadastros"]
        self.assertEqual(cadastros.count(), Pessoa.objects.count())
