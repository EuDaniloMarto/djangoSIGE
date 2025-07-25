from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .services import get_quantidade_cadastro, get_agenda_hoje, get_alertas, get_movimento_e_saldo


@login_required
def pagina_inicial(request):
    template_name = 'base/index.html'

    hoje = datetime.now().date()

    context = {
        "data_atual": hoje.strftime('%d/%m/%Y'),
        "quantidade_cadastro": get_quantidade_cadastro(),
        "agenda_hoje": get_agenda_hoje(hoje),
        "alertas": get_alertas(hoje),
        **get_movimento_e_saldo(hoje),
    }

    return render(request, template_name, context)


def handler404(request):
    return render(request, '404.html', status_code=404)


def handler500(request):
    return render(request, '500.html', status_code=500)
