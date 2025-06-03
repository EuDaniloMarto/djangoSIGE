from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .services import (
    contagem_eventos_agendados_dia_hoje,
    movimento_caixa_hoje,
    quantidade_total_registros_entidades_principais,
    situacoes_criticas_para_exibir_alertas_na_dashboard,
)


@login_required
def dashboard_index(request: HttpRequest) -> HttpResponse:
    template_name = "dashboard/dashboard_index.html"
    data_hoje = date.today()
    context = {
        "data_atual": data_hoje.strftime("%d/%m/%Y"),
        "quantidade_cadastro": quantidade_total_registros_entidades_principais(),
        "agenda_hoje": contagem_eventos_agendados_dia_hoje(data_hoje),
        "alertas": situacoes_criticas_para_exibir_alertas_na_dashboard(data_hoje),
    }
    context.update(movimento_caixa_hoje(data_hoje))
    return render(request, template_name, context)
