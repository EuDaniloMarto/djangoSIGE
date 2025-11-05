from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from djangosige.cadastros.pessoas.tests.factories import PessoaFactory
from djangosige.cadastros.views import EditarCadastro


class TestUrlEditarCadastro(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pessoa = PessoaFactory.create()

    def setUp(self):
        self.resolver = resolve(reverse("cadastros:editar_cadastro", kwargs={"pk": self.pessoa.pk}))

    def test_a_URL_deve_resolver_para_a_classe_de_view_correta(self):
        self.assertEqual(self.resolver.func.view_class, EditarCadastro)

    def test_o_nome_da_URL_deve_ser_editar_cadastro(self):
        self.assertEqual(self.resolver.url_name, "editar_cadastro")

    def test_o_namespace_deve_ser_cadastros(self):
        self.assertEqual(self.resolver.app_name, "cadastros")

    def test_a_rota_da_URL_deve_ser_n_cadastros_editar_pk(self):
        self.assertEqual(self.resolver.route, "n/cadastros/<int:pk>/editar/")


class TestAcessoEditarCadastro(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="johndoe", password="john@doe.test")
        cls.pessoa = PessoaFactory.create(colaborador=cls.user)
        cls.url = reverse("cadastros:editar_cadastro", kwargs={"pk": cls.pessoa.pk})

    def test_o_usuario_nao_autenticado_deve_receber_codigo_de_redirecionamento(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_o_usuario_nao_autenticado_deve_ser_redirecionado_para_a_tela_de_login(self):
        response = self.client.get(self.url)
        self.assertIn("/login/", response.url)

    def test_a_view_deve_retornar_HTTP_200_para_usuarios_autenticados(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestContextoEditarCadastro(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="johndoe", password="john@doe.test")
        cls.pessoa = PessoaFactory.create(colaborador=cls.user)
        cls.url = reverse("cadastros:editar_cadastro", kwargs={"pk": cls.pessoa.pk})

    def setUp(self):
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_o_nome_do_template_usado(self):
        self.assertTemplateUsed(self.response, "cadastros/editar_cadastro.html")

    def test_a_palavra_chave_pagina_deve_estar_no_contexto(self):
        self.assertIn("pagina", self.response.context)

    def test_o_valor_da_palavra_chave_pagina_eh_cadastro(self):
        self.assertEqual(self.response.context["pagina"], "cadastros")

    def test_a_palavra_chave_cadastro_deve_estar_no_contexto(self):
        self.assertIn("cadastro", self.response.context)

    def test_o_cadastro_no_contexto_deve_corresponder_ao_pk_da_URL(self):
        self.assertEqual(self.response.context["cadastro"].pk, self.pessoa.pk)


class TestFormularioEditarCadastro(TestCase):
    def test_o_form_class_deve_ser_uma_ModelForm_de_Pessoa(self):
        form_class = EditarCadastro.form_class
        self.assertTrue(issubclass(form_class, forms.ModelForm))

    def test_os_campos_do_form_devem_ser_os_definidos_na_view(self):
        expected_fields = [
            "descricao",
            "tipo_pessoa",
            "eh_cliente",
            "eh_fornecedor",
            "eh_transportadora",
            "ativo",
            "observacoes",
        ]
        form_class = EditarCadastro.form_class
        self.assertListEqual(list(form_class().fields), expected_fields)


class TestEditarCadastroPost(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="johndoe", password="john@doe.test")
        cls.pessoa = PessoaFactory.create(
            descricao="Pessoa Antiga",
            tipo_pessoa="PJ",
            colaborador=cls.user,
        )
        cls.url = reverse("cadastros:editar_cadastro", kwargs={"pk": cls.pessoa.pk})

    def setUp(self):
        self.client.force_login(self.user)

    def test_um_cadastro_eh_editado_com_sucesso(self):
        data = {
            "descricao": "Pessoa Atualizada",
            "tipo_pessoa": "PF",
            "eh_cliente": True,
            "eh_fornecedor": False,
            "eh_transportadora": False,
            "ativo": True,
            "observacoes": "Atualizado via teste",
        }
        self.client.post(self.url, data)
        self.pessoa.refresh_from_db()
        self.assertEqual(self.pessoa.descricao, "Pessoa Atualizada")


class TestEditarCadastroFormularioInvalido(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="johndoe", password="john@doe.test"
        )
        cls.pessoa = PessoaFactory.create(
            descricao="Pessoa Antiga",
            tipo_pessoa="PJ",
            colaborador=cls.user,
        )
        cls.url = reverse("cadastros:editar_cadastro", kwargs={"pk": cls.pessoa.pk})

    def setUp(self):
        self.client.force_login(self.user)
        # Envia um POST inválido (campo obrigatório em branco)
        self.response = self.client.post(
            self.url,
            {
                "descricao": "",  # <- inválido
                "tipo_pessoa": "PF",
                "eh_cliente": True,
                "eh_fornecedor": False,
                "eh_transportadora": False,
                "ativo": True,
                "observacoes": "Teste inválido",
            },
        )

    def test_o_status_code_deve_ser_200_para_formulario_invalido(self):
        self.assertEqual(self.response.status_code, 200)

    def test_o_template_usado_para_formulario_invalido_deve_ser_editar_cadastro_html(self):
        self.assertTemplateUsed(self.response, "cadastros/editar_cadastro.html")

    def test_o_formulario_deve_conter_erros(self):
        form = self.response.context["form"]
        self.assertTrue(form.errors)

    def test_o_formulario_deve_conter_erro_no_campo_descricao(self):
        form = self.response.context["form"]
        self.assertIn("descricao", form.errors)

    def test_o_erro_do_campo_descricao_deve_ser_mensagem_padrao_de_obrigatoriedade(self):
        form = self.response.context["form"]
        self.assertIn("Este campo é obrigatório.", form.errors["descricao"])
