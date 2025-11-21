from http import HTTPStatus

import pytest
from django.db.models import QuerySet
from django.urls import reverse

from ..models import Pessoa


@pytest.mark.django_db
def test_o_usuario_que_nao_estiver_logado_nao_acessa_a_pagina_de_listagem_dos_cadastros(client):
    response = client.get(reverse("cadastros:listar"))
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_a_url_que_o_usuario_nao_logado_e_redirecionado_quando_tentar_acessar_a_pagina_de_listagem_dos_cadastros(
    client,
):
    response = client.get(reverse("cadastros:listar"))
    assert response.url == "/login/"


@pytest.mark.django_db
def test_o_usuario_logado_pode_acessar_a_pagina_de_listagem_dos_cadastros(client_logged):
    response = client_logged.get(reverse("cadastros:listar"))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_o_nome_do_template_usado_para_renderizar_a_pagina_de_listagem_dos_cadastros(client_logged):
    response = client_logged.get(reverse("cadastros:listar"))
    assert "cadastros/listar.html" in [template.name for template in response.templates]


@pytest.mark.django_db
def test_a_palavra_chave_pagina_deve_estar_no_contexto_da_resposta_da_listagem_de_cadastros(client_logged):
    response = client_logged.get(reverse("cadastros:listar"))
    assert "pagina" in response.context


@pytest.mark.django_db
def test_o_valor_da_palavra_chave_pagina_deve_ser_cadastros_no_contexto_da_resposta_da_listagem_de_cadastros(
    client_logged,
):
    response = client_logged.get(reverse("cadastros:listar"))
    assert response.context["pagina"] == "cadastros"


@pytest.mark.django_db
def test_a_palavra_chave_cadastros_deve_estar_no_contexto_da_resposta_da_listagem_de_cadastros(client_logged):
    response = client_logged.get(reverse("cadastros:listar"))
    assert "cadastros" in response.context


@pytest.mark.django_db
def test_o_valor_da_palavra_chave_cadastros_deve_ser_um_queryset_no_context_da_resposta_da_listagem_de_cadastros(
    client_logged,
):
    response = client_logged.get(reverse("cadastros:listar"))
    assert isinstance(response.context["cadastros"], QuerySet)


@pytest.mark.django_db
def test_o_valor_do_queryset_de_ser_do_model_pessoa_no_context_da_resposta_da_listagem_de_cadastros(client_logged):
    response = client_logged.get(reverse("cadastros:listar"))
    queryset = response.context["cadastros"]
    assert queryset.model == Pessoa


@pytest.mark.django_db
def test_deve_haver_a_palavra_chave_relacionamento_no_context_da_resposta_da_listagem_de_cadastros(client_logged):
    response = client_logged.get(reverse("cadastros:listar"))
    assert "relacionamento" in response.context


@pytest.mark.django_db
def test_o_valor_padrao_da_palavra_chave_e_none_no_context_da_resposta_da_listagem_de_cadastros(client_logged):
    response = client_logged.get(reverse("cadastros:listar"))
    assert not response.context["relacionamento"]


@pytest.mark.django_db
@pytest.mark.parametrize("relacionamento", ["cliente", "fornecedor", "transportadora"])
def test_os_valores_validos_da_palavra_chave_relacionamento_no_context_da_resposta_da_listagem_de_cadastros(
    relacionamento, client_logged
):
    response = client_logged.get(reverse("cadastros:listar"), {"relacionamento": relacionamento})
    assert response.context["relacionamento"] == relacionamento


@pytest.mark.django_db
def test_qualquer_valor_que_nao_for_os_valores_validos_para_a_palavra_chave_dever_ser_none_no_context_da_resposta_da_listagem_de_cadastros(
    client_logged,
):
    response = client_logged.get(reverse("cadastros:listar"), {"relacionamento": "xpto"})
    assert not response.context["relacionamento"]
