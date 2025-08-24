"""
Este módulo define visualizações para o painel principal e manipuladores de erros na aplicação Django.

Classes:
PaginaInicial (LoginRequiredMixin, TemplateView):
Exibe a página principal do painel para usuários autenticados.
Preenche o contexto do template com:
- quantidade_cadastro: Número total de cadastros.
- agenda_hoje: Itens da agenda agendados para hoje.
- alertas: Alertas relevantes para a data atual.
- data_atual: Data atual formatada como DD/MM/AAAA.
- movimento_caixa: Dados de movimentação financeira para a data atual.

Funções:
handler404(request):
Renderiza a página de erro 404 personalizada com status HTTP 404.

handler500(request):
Renderiza a página de erro 500 personalizada com status HTTP 500.
"""

from datetime import datetime
from http import HTTPStatus

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from .services import quantidade_cadastros, alertas, agenda_do_dia, movimento_caixa


class PaginaInicial(LoginRequiredMixin, TemplateView):
    """
    IndexView exibe a página principal do painel para usuários autenticados.

    Esta visualização estende a TemplateView do Django e requer autenticação do usuário.
    Ela preenche o contexto do template com:
    - quantidade_cadastro: O número total de inscrições.
    - agenda_hoje: Os itens da agenda agendados para hoje.
    - alertas: Alertas relevantes para a data atual.
    - data_atual: A data atual formatada como DD/MM/AAAA.
    - movimento_caixa: Dados de movimentação financeira para a data atual.

    Todos os dados de contexto são gerados dinamicamente para a data atual.
    """

    template_name = "pagina_inicial.html"

    def get_context_data(self, **kwargs):
        data_atual = datetime.now().date()

        kwargs.update(
            {
                "quantidade_cadastro": quantidade_cadastros(),
                "agenda_hoje": agenda_do_dia(data_atual),
                "alertas": alertas(data_atual),
                "data_atual": data_atual.strftime("%d/%m/%Y"),
                **movimento_caixa(data_atual),
            }
        )

        return super().get_context_data(**kwargs)


pagina_inicial = PaginaInicial.as_view()


def handler404(request):
    """
    Manipulador personalizado para erros HTTP 404.

    Argumentos:
    requisição (HttpRequest): A requisição HTTP recebida que acionou o erro 404.

    Retorna:
    HttpResponse: Página de erro 404 renderizada com código de status HTTP 404 (Não Encontrado).
    """
    return render(request, "404.html", status=HTTPStatus.NOT_FOUND)


def handler500(request):
    """
    Lida com respostas de erro interno do servidor HTTP 500.

    Renderiza o modelo '500.html' com um código de status 500 quando ocorre um erro do servidor.

    Argumentos:
    request (HttpRequest): A solicitação HTTP recebida.

    Retorna:
    HttpResponse: A página de erro 500 renderizada com status HTTP 500.
    """
    return render(request, "500.html", status=HTTPStatus.INTERNAL_SERVER_ERROR)
