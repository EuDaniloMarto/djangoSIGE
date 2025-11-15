from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_o_usuario_que_nao_estiver_logado_nao_acessa_a_pagina_de_listagem_dos_cadastros(client):
    """O usuário que não estiver logado não acessa a página de listagem dos cadastros."""
    response = client.get(reverse("cadastros:listar"))
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_a_url_que_o_usuario_nao_logado_e_redirecionado_quando_tentar_acessar_a_pagina_de_listagem_dos_cadastros(
    client,
):
    """A URL que o usuário não logado é redirecionado quando tentar acessar a página de listagem dos cadastros"""

    response = client.get(reverse("cadastros:listar"))
    assert response.url == "/login/"


@pytest.mark.django_db
def test_o_usuario_logado_pode_acessar_a_pagina_de_listagem_dos_cadastros(client_logged):
    """O usuário logado pode acessar a página de listagem dos cadastros."""

    response = client_logged.get(reverse("cadastros:listar"))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_o_nome_do_template_usado_para_renderizar_a_pagina_de_listagem_dos_cadastros(client_logged):
    """O nome do template usado para renderizar a página de listagem dos cadastros."""

    response = client_logged.get(reverse("cadastros:listar"))
    assert "cadastros/listar.html" in [template.name for template in response.templates]


@pytest.mark.django_db
def test_a_palavra_chave_pagina_deve_estar_no_contexto_da_resposta_da_listagem_de_cadastros(client_logged):
    """A palavra chave 'página' deve estar no contexto da resposta da litagem de cadastros."""

    response = client_logged.get(reverse("cadastros:listar"))
    assert "pagina" in response.context


@pytest.mark.django_db
def test_o_valor_da_palavra_chave_pagina_deve_ser_cadastros_no_contexto_da_resposta_da_listagem_de_cadastros(
    client_logged,
):
    """O valor da palavra chave 'página' deve ser 'cadastros' no contexto da resposta da listagem de cadastros."""

    response = client_logged.get(reverse("cadastros:listar"))
    assert response.context["pagina"] == "cadastros"


@pytest.mark.django_db
def test_o_usuario_que_nao_estiver_logado_nao_acessa_a_pagina_para_criar_um_cadastro(client):
    """O usuário que não estiver logado não acessa a página de criação dos cadastros."""
    response = client.get(reverse("cadastros:criar"))
    assert response.status_code == HTTPStatus.FOUND  # Espera-se 302 (Redirecionamento)


@pytest.mark.django_db
def test_a_url_que_o_usuario_nao_logado_e_redirecionado_quando_tentar_acessar_a_pagina_para_criar_um_cadastro(
    client,
):
    """A URL que o usuário não logado é redirecionado quando tentar acessar a página de criação dos cadastros."""
    response = client.get(reverse("cadastros:criar"))
    # A URL deve ser o caminho para o login
    assert response.url.startswith("/login/")


@pytest.mark.django_db
def test_o_usuario_logado_pode_acessar_a_pagina_para_criar_um_cadastro(client_logged):
    """O usuário logado pode acessar a página para criar um cadastro."""
    response = client_logged.get(reverse("cadastros:criar"))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_o_nome_do_template_usado_para_renderizar_a_pagina_para_criar_um_cadastro(client_logged):
    """O nome do template usado para renderizar a página para criar um cadastro."""
    response = client_logged.get(reverse("cadastros:criar"))
    assert "cadastros/criar.html" in [template.name for template in response.templates]


@pytest.mark.django_db
def test_a_palavra_chave_pagina_deve_estar_no_contexto_da_resposta_para_criar_um_cadastro(client_logged):
    """A palavra chave 'pagina' deve estar no contexto da resposta da página para criar um cadastro."""
    response = client_logged.get(reverse("cadastros:criar"))
    assert "pagina" in response.context


@pytest.mark.django_db
def test_o_valor_da_palavra_chave_pagina_deve_ser_cadastros_no_contexto_da_resposta_para_criar_um_cadastro(
    client_logged,
):
    """O valor da palavra chave 'pagina' deve ser 'cadastros' no contexto da resposta da página para criar um cadastro."""
    response = client_logged.get(reverse("cadastros:criar"))
    assert response.context["pagina"] == "cadastros"
