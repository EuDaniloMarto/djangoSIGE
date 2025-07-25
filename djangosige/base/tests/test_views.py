from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


UserModel = get_user_model()


class TestUsuarioNaoAutenticado(TestCase):
    """Testes para verificar o comportamento de usuários não autenticados."""

    def test_status_code_302(self):
        """
        Verifica se um usuário não autenticado é redirecionado (status 302)
        ao tentar acessar a página inicial.
        """
        response = self.client.get(reverse('base:index'))
        self.assertEqual(response.status_code, 302)


class TestUsuarioAutenticado(TestCase):
    """Testes para verificar o comportamento de usuários autenticados"""

    def setUp(self):
        """
        Configura o ambiente de teste: cria um usuário e o autentica.
        """
        self.user = UserModel.objects.create_user(username='johndoe', password='senha@johndoe')
        self.client.login(username='johndoe', password='senha@johndoe')

    def test_status_code_200(self):
        """
        Verifica se um usuário autenticado acessa a página com sucesso (status 200).
        """
        response = self.client.get(reverse('base:index'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """
        Verifica se o template correto está sendo usado.
        """
        response = self.client.get(reverse('base:index'))
        self.assertTemplateUsed(response, 'base/index.html')

    def test_palavra_chave_quantidade_cadastro_esta_no_context_da_resposta(self):
        """Verifica se a chave 'quantidade_cadastro' está presente no contexto da resposta."""
        response = self.client.get(reverse('base:index'))
        self.assertIn('quantidade_cadastro', response.context)

    def test_palavra_chave_agenda_hoje_esta_no_context_da_resposta(self):
        """Verifica se a chave 'agenda_hoje' está presente no contexto da resposta."""
        response = self.client.get(reverse('base:index'))
        self.assertIn('agenda_hoje', response.context)

    def test_palavra_chave_alertas_esta_no_context_da_resposta(self):
        """Verifica se a chave 'alertas' está presente no contexto da resposta."""
        response = self.client.get(reverse('base:index'))
        self.assertIn('alertas', response.context)

    def test_palavra_chave_movimento_dia_esta_no_context_da_resposta(self):
        """Verifica se a chave 'movimento_dia' está presente no contexto da resposta."""
        response = self.client.get(reverse('base:index'))
        self.assertIn('movimento_dia', response.context)

    def test_palavra_chave_saldo_esta_no_context_da_resposta(self):
        """Verifica se a chave 'saldo' está presente no contexto da resposta."""
        response = self.client.get(reverse('base:index'))
        self.assertIn('saldo', response.context)
