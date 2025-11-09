import pytest
from brutils import generate_cnpj, generate_cpf
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ..choices import EscolherBanco
from ..models import (
    Banco,
    Documento,
    Email,
    Endereco,
    Pessoa,
    PessoaFisica,
    PessoaJuridica,
    Site,
    Telefone,
)
from .factories import (
    BancoFactory,
    EmailFactory,
    EnderecoFactory,
    PessoaFactory,
    SiteFactory,
    TelefoneFactory,
)


@pytest.fixture
def pessoa():
    return PessoaFactory(tipo_pessoa=Pessoa.EscolherTipoPessoa.PF)


@pytest.fixture
def pessoa_pf():
    """Fixture para criar uma Pessoa Física (PF)"""
    return PessoaFactory(tipo_pessoa=Pessoa.EscolherTipoPessoa.PF)


@pytest.fixture
def pessoa_pj():
    """Fixture para criar uma Pessoa Jurídica (PJ)"""
    return PessoaFactory(tipo_pessoa=Pessoa.EscolherTipoPessoa.PJ)


PRINCIPAL_MODELS = [
    (Endereco, EnderecoFactory, "Endereço"),
    (Telefone, TelefoneFactory, "Telefone"),
    (Email, EmailFactory, "Email"),
    (Site, SiteFactory, "Site"),
    (Banco, BancoFactory, "Banco"),
]


@pytest.mark.django_db
def test_uma_pessoa_do_tipo_pf_e_criada_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_pessoa(user):
    """Uma pessoa é criada com sucesso quando todos os dados são enviados para o model Pessoa"""

    # Dados fekes gerados em https://www.4devs.com.br/gerador_de_pessoas
    Pessoa.objects.create(
        colaborador=user,
        descricao="Fátima Luciana Nair Novaes",
        tipo_pessoa=Pessoa.EscolherTipoPessoa.PF,
        e_cliente=True,
        e_fornecedor=True,
        e_transportadora=True,
        esta_ativo=True,
        observacoes="Lorem ipsum dolor sit amet, consectetur adipiscing elit",
    )

    assert Pessoa.objects.count() == 1


@pytest.mark.django_db
def test_uma_pessoa_do_tipo_pj_e_criada_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_pessoa(user):
    """Uma pessoa é criada com sucesso quando todos os dados são enviados para o model Pessoa"""

    # Dados fekes gerados em https://www.4devs.com.br/gerador_de_empresas
    Pessoa.objects.create(
        colaborador=user,
        descricao="Benedito e Lara Telas ME",
        tipo_pessoa=Pessoa.EscolherTipoPessoa.PJ,
        e_cliente=True,
        e_fornecedor=True,
        e_transportadora=True,
        esta_ativo=True,
        observacoes="Lorem ipsum dolor sit amet, consectetur adipiscing elit",
    )
    assert Pessoa.objects.count() == 1


@pytest.mark.django_db
def test_uma_pessoa_e_criada_com_sucesso_quando_apenas_os_dados_essenciais_para_o_cadastro_sao_enviados_para_o_model_pessoa(
    user,
):
    """Uma pessoa é criada com sucesso quando apenas os dados essenciais para o cadastro são enviados para o model Pessoa."""

    Pessoa.objects.create(
        colaborador=user,
        descricao="Fátima Luciana Nair Novaes",
        tipo_pessoa=Pessoa.EscolherTipoPessoa.PF,
    )

    assert Pessoa.objects.count() == 1


@pytest.mark.django_db
def test_uma_pessoa_nao_deve_ser_criada_quando_o_campo_colaborador_nao_for_enviado_para_o_model_pessoa():
    """Uma pessoa não deve ser criada quando o campo 'colaborador' não for enviado_para_model_pessoa."""

    p = Pessoa(
        descricao="Benedito e Lara Telas ME",
        tipo_pessoa=Pessoa.EscolherTipoPessoa.PJ,
    )
    with pytest.raises(ValidationError) as e:
        p.full_clean()

    assert "{'colaborador': ['Este campo não pode ser nulo.']}" == str(e.value)


@pytest.mark.django_db
def test_uma_pessoa_nao_deve_ser_criada_quando_o_campo_descricao_nao_for_enviado_para_o_model_pessoa(user):
    """Uma pessoa não deve ser criada quando o campo 'descrição' não for enviado para o model Pessoa."""

    p = Pessoa(
        colaborador=user,
        tipo_pessoa=Pessoa.EscolherTipoPessoa.PF,
    )
    with pytest.raises(ValidationError) as e:
        p.full_clean()

    assert "{'descricao': ['Este campo não pode estar vazio.']}" == str(e.value)


@pytest.mark.django_db
def test_uma_pessoa_nao_deve_ser_criada_quando_o_valor_da_descricao_enviado_para_o_model_pessoa_ja_estiver_cadastrado(
    user,
):
    """Uma pessoa não deve ser criada quando o valor da descricao enviado para o model Pessoa já estiver cadastro."""

    descricao = "Fátima Luciana Nair Novaes"
    PessoaFactory(descricao=descricao)

    p = Pessoa(
        colaborador=user,
        descricao=descricao,
        tipo_pessoa=Pessoa.EscolherTipoPessoa.PF,
    )
    with pytest.raises(ValidationError) as e:
        p.full_clean()
    assert "{'descricao': ['Pessoa com este Descrição já existe.']}" == str(e.value)


@pytest.mark.django_db
def test_uma_pessoa_fisica_deve_ser_criada_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_pessoa_fisica(
    pessoa,
):
    """Uma pessoa física deve ser criada com sucesso quando todos os dados são enviados para o model PessoaFisica."""

    # Dados fekes gerados em https://www.4devs.com.br/gerador_de_pessoas
    PessoaFisica.objects.create(
        pessoa=pessoa,
        cpf="726.614.489-26",
        rg="48.492.227-0",
        nascimento="1950-09-08",
    )

    assert PessoaFisica.objects.count() == 1


@pytest.mark.django_db
def test_uma_pessoa_fisica_deve_ser_criada_com_sucesso_quando_apenas_os_dados_essenciais_sao_enviados_para_o_model_pessoa_fisica(
    pessoa,
):
    """Uma pessoa física deve ser criada com sucesso quando apenas os dados essenciais são enviados para o model PessoaFisica."""

    PessoaFisica.objects.create(pessoa=pessoa)
    assert PessoaFisica.objects.count() == 1


@pytest.mark.django_db
def test_uma_pessoa_fisica_deve_ser_criada_com_sucesso_quando_o_cpf_enviado_para_o_model_pessoa_fisica_e_valido(pessoa):
    """Uma pessoa física deve ser criada com sucesso quando o CPF enviado para o model PessoaFisica é válido."""

    PessoaFisica.objects.create(pessoa=pessoa, cpf=generate_cpf())
    assert PessoaFisica.objects.count() == 1


@pytest.mark.django_db
def test_uma_pessoa_fisica_nao_deve_ser_criada_quando_nao_for_enviado_para_o_model_pessoa_fisica_o_campo_pessoa():
    """Uma pessoa física não deve ser criada quando não for enviado para o model PessoaFísica o campo 'pessoa'."""

    with pytest.raises(IntegrityError) as e:
        PessoaFisica.objects.create()
    assert "NOT NULL constraint failed: cadastros_pessoafisica.pessoa_id" == str(e.value)


@pytest.mark.django_db
def test_uma_pessoa_fisica_nao_deve_ser_criada_quando_o_cpf_enviado_para_o_model_pessoa_fisica_e_invalido(pessoa):
    """Uma pessoa física não deve ser criada quando o CPF enviado para o model PessoaFisica é inválido."""

    pf = PessoaFisica(pessoa=pessoa, cpf="123.456.789-00")
    with pytest.raises(ValidationError) as e:
        pf.full_clean()

    assert "cpf" in e.value.message_dict


@pytest.mark.django_db
def test_nao_deve_ser_possivel_criar_duas_pessoas_fisicas_com_o_mesmo_cpf_valido(pessoa_pf):
    """Uma Pessoa Física não deve ser criada quando o CPF já estiver cadastrado (unicidade)."""

    cpf_valido = generate_cpf()
    PessoaFisica.objects.create(pessoa=pessoa_pf, cpf=cpf_valido)

    pessoa2 = PessoaFactory(descricao="Outra Pessoa", tipo_pessoa=Pessoa.EscolherTipoPessoa.PF)
    pf2 = PessoaFisica(pessoa=pessoa2, cpf=cpf_valido)

    with pytest.raises(ValidationError) as e:
        pf2.full_clean()

    e.value.message_dict
    assert "cpf" in e.value.message_dict


@pytest.mark.django_db
def test_get_absolute_url_retorna_a_url_de_detalhes_correta(pessoa_pf):
    """Verifica se o método get_absolute_url retorna a URL de visualização correta."""
    pk = pessoa_pf.pk
    expected_url = f"/cadastros/{pk}/"

    assert pessoa_pf.get_absolute_url() == expected_url


@pytest.mark.django_db
def test_get_absolute_update_url_retorna_a_url_de_edicao_correta(pessoa_pf):
    """Verifica se o método get_absolute_update_url retorna a URL de edição correta."""
    pk = pessoa_pf.pk
    expected_url = f"/cadastros/{pk}/editar/"

    assert pessoa_pf.get_absolute_update_url() == expected_url


@pytest.mark.django_db
def test_uma_pessoa_juridica_deve_ser_criada_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_pessoa_juridica(
    pessoa,
):
    """Uma pessoa jurídica deve ser criada com sucesso quando todos os dados são enviados para o model PessoaJuridica."""

    # Dados fekes gerados em https://www.4devs.com.br/gerador_de_empresas
    PessoaJuridica.objects.create(
        pessoa=pessoa,
        nome_fantasia="Sabrina e Mariana Financeira ME",
        cnpj="54.806.817/0001-80",
        inscricao_municipal="123.456.789",
        inscricao_estadual="253.566.998.314",
        proprietario="Sabrina",
        situacao_fiscal=PessoaJuridica.EscolherEnquadramentoFiscal.SN,
        suframa="30.20.00.01-0",
    )

    assert PessoaJuridica.objects.count() == 1


@pytest.mark.django_db
def test_uma_pessoa_juridica_deve_ser_criada_com_sucesso_quando_apenas_os_dados_essenciais_sao_enviados_para_o_model_pessoa_juridica(
    pessoa,
):
    """Uma pessoa jurídica deve ser criada com sucesso quando apenas os dados essenciais são enviados para o model PessoaJuridica."""

    PessoaJuridica.objects.create(pessoa=pessoa)
    assert PessoaJuridica.objects.count() == 1


@pytest.mark.django_db
def test_uma_pessoa_juridica_deve_ser_criada_com_sucesso_quando_o_cnpj_enviado_para_o_model_pessoa_juridica_e_valido(
    pessoa,
):
    """Uma pessoa juridica deve ser criada com sucesso quando o CNPJ enviado para o model PessoaJuridica é válido."""

    PessoaJuridica.objects.create(pessoa=pessoa, cnpj=generate_cnpj())
    assert PessoaJuridica.objects.count() == 1


@pytest.mark.django_db
def test_uma_pessoa_juridica_nao_deve_ser_criada_quando_o_campo_pessoa_nao_for_enviado_para_o_model_pessoa_juridica():
    """Uma pessoa jurídica não deve ser criada quando o campo 'pessoa' não for enviado para o model PessoaJuridica."""

    with pytest.raises(IntegrityError) as e:
        PessoaJuridica.objects.create()
    assert "NOT NULL constraint failed: cadastros_pessoajuridica.pessoa_id" == str(e.value)


@pytest.mark.django_db
def test_uma_pessoa_juridica_nao_deve_ser_criada_quando_o_cnpj_enviado_para_o_model_pessoa_juridica_e_invalido(pessoa):
    """Uma pessoa jurídica não deve ser criada quando o CNPJ enviado para o model PessoaJuridica é inválido."""

    pj = PessoaJuridica(pessoa=pessoa, cnpj="12.345.678/0001-00")
    with pytest.raises(ValidationError) as e:
        pj.full_clean()

    assert "cnpj" in e.value.message_dict


@pytest.mark.django_db
def test_nao_deve_ser_possivel_criar_duas_pessoas_juridicas_com_o_mesmo_cnpj_valido(pessoa_pj):
    """Uma Pessoa Jurídica não deve ser criada quando o CNPJ já estiver cadastrado (unicidade)."""
    cnpj_valido = generate_cnpj()
    PessoaJuridica.objects.create(pessoa=pessoa_pj, cnpj=cnpj_valido)

    pessoa2 = PessoaFactory(descricao="Outra Empresa", tipo_pessoa=Pessoa.EscolherTipoPessoa.PJ)
    pj2 = PessoaJuridica(pessoa=pessoa2, cnpj=cnpj_valido)

    with pytest.raises(ValidationError) as e:
        pj2.full_clean()

    assert "cnpj" in e.value.message_dict


@pytest.mark.django_db
def test_um_endereco_deve_ser_criado_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_endereco(pessoa):
    """Um endereço deve ser criado com sucesso quando todos os dados são enviados para o model Endereço."""

    # https://www.4devs.com.br/gerador_de_pessoas
    Endereco.objects.create(
        pessoa=pessoa,
        logradouro="Rua Maria do Rosário Silva",
        numero="Rua Maria do Rosário Silva",
        complemento="",
        bairro="José Américo de Almeida",
        municipio="João Pessoa",
        uf="PB",
        pais="Brasil",
        cep="58074-726",
        e_entrega=True,
        e_cobranca=True,
    )
    assert Endereco.objects.count() == 1


@pytest.mark.django_db
def test_um_endereco_deve_ser_criado_com_sucesso_quando_apenas_os_dados_essenciais_sao_enviados_para_o_model_endereco(
    pessoa,
):
    """Um endereçe deve ser criado com sucesso quando apenas os dados essenciais são enviados para o model Endereço."""

    Endereco.objects.create(pessoa=pessoa)
    assert Endereco.objects.count() == 1


@pytest.mark.django_db
def test_um_endereco_nao_deve_ser_criado_quando_o_campo_pessoa_nao_for_enviado_para_o_model_endereco():
    """Um endereço não deve ser criado quando o campo 'pessoa' não for enviado para o model Endereço."""

    with pytest.raises(IntegrityError) as e:
        Endereco.objects.create()

    assert "NOT NULL constraint failed: cadastros_endereco.pessoa_id" == str(e.value)


@pytest.mark.django_db
def test_um_telefone_deve_ser_criado_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_telefone(pessoa):
    """Um telefone deve ser criado com sucesso quando todos os dados são enviados para o model Telefone."""

    # https://www.4devs.com.br/gerador_de_pessoas
    Telefone.objects.create(
        pessoa=pessoa,
        telefone="(83) 91234-5678",
    )
    assert Telefone.objects.count() == 1


@pytest.mark.django_db
def test_um_telefone_deve_ser_criado_com_sucesso_quando_apenas_os_dados_essenciais_sao_enviados_para_o_model_telefone(
    pessoa,
):
    """Um telefone deve ser criado com sucesso quando apenas os dados essenciais são enviados para o model Telefone."""

    Telefone.objects.create(pessoa=pessoa)
    assert Telefone.objects.count() == 1


@pytest.mark.django_db
def test_um_telefone_nao_deve_ser_criado_quando_o_campo_pessoa_nao_for_enviado_para_o_model_telefone():
    """Um telefone não deve ser criado quando o campo 'pessoa' não for enviado para o model Telefone."""

    with pytest.raises(IntegrityError) as e:
        Telefone.objects.create()

    assert "NOT NULL constraint failed: cadastros_telefone.pessoa_id" == str(e.value)


@pytest.mark.django_db
def test_um_email_deve_ser_criado_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_email(pessoa):
    """Um email deve ser criado com sucesso quando todos os dados são enviados para o model Email."""

    # https://www.4devs.com.br/gerador_de_pessoas
    Email.objects.create(pessoa=pessoa, email="isadora_stefany_aragao@acramisper.com")
    assert Email.objects.count() == 1


@pytest.mark.django_db
def test_um_email_deve_ser_criado_com_sucesso_quando_apenas_os_dados_essenciais_sao_enviados_para_o_model_email(
    pessoa,
):
    """Um email deve ser criado com sucesso quando apenas os dados essenciais são enviados para o model Email."""

    Email.objects.create(pessoa=pessoa)
    assert Email.objects.count() == 1


@pytest.mark.django_db
def test_um_email_nao_deve_ser_criado_quando_o_campo_pessoa_nao_for_enviado_para_o_model_email():
    """Um email não deve ser criado quando o campo 'pessoa' não for enviado para o model Email."""

    with pytest.raises(IntegrityError) as e:
        Email.objects.create()

    assert "NOT NULL constraint failed: cadastros_email.pessoa_id" == str(e.value)


@pytest.mark.django_db
def test_um_site_deve_ser_criado_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_site(pessoa):
    """Um site deve ser criado com sucesso quando todos os dados são enviados para o model Site."""

    # https://www.4devs.com.br/gerador_de_pessoas
    Site.objects.create(pessoa=pessoa, site="www.acramisper.com")
    assert Site.objects.count() == 1


@pytest.mark.django_db
def test_um_site_deve_ser_criado_com_sucesso_quando_apenas_os_dados_essenciais_sao_enviados_para_o_model_site(
    pessoa,
):
    """Um site deve ser criado com sucesso quando apenas os dados essenciais são enviados para o model Site."""

    Site.objects.create(pessoa=pessoa)
    assert Site.objects.count() == 1


@pytest.mark.django_db
def test_um_site_nao_deve_ser_criado_quando_o_campo_pessoa_nao_for_enviado_para_o_model_site():
    """Um site não deve ser criado quando o campo 'pessoa' não for enviado para o model Site."""

    with pytest.raises(IntegrityError) as e:
        Site.objects.create()

    assert "NOT NULL constraint failed: cadastros_site.pessoa_id" == str(e.value)


@pytest.mark.django_db
def test_um_banco_deve_ser_criado_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_banco(pessoa):
    """Um banco deve ser criado com sucesso quando todos os dados são enviados para o model Banco."""

    # https://www.4devs.com.br/gerador_de_pessoas
    Banco.objects.create(pessoa=pessoa, banco=EscolherBanco.BB, agencia="1234-5", conta="67890", digito="1")
    assert Banco.objects.count() == 1


@pytest.mark.django_db
def test_um_banco_deve_ser_criado_com_sucesso_quando_apenas_os_dados_essenciais_sao_enviados_para_o_model_banco(
    pessoa,
):
    """Um banco deve ser criado com sucesso quando apenas os dados essenciais são enviados para o model Banco."""

    Banco.objects.create(pessoa=pessoa)
    assert Banco.objects.count() == 1


@pytest.mark.django_db
def test_um_banco_nao_deve_ser_criado_quando_o_campo_pessoa_nao_for_enviado_para_o_model_banco():
    """Um banco não deve ser criado quando o campo 'pessoa' não for enviado para o model Banco."""

    with pytest.raises(IntegrityError) as e:
        Banco.objects.create()

    assert "NOT NULL constraint failed: cadastros_banco.pessoa_id" == str(e.value)


@pytest.mark.django_db
def test_um_documento_deve_ser_criado_com_sucesso_quando_todos_os_dados_sao_enviados_para_o_model_documento(pessoa):
    """Um documento deve ser criado com sucesso quando todos os dados são enviados para o model Documento."""

    # https://www.4devs.com.br/gerador_de_pessoas
    Documento.objects.create(
        pessoa=pessoa,
        documento="Contrato de Prestação de Serviços",
    )
    assert Documento.objects.count() == 1


@pytest.mark.django_db
def test_um_documento_deve_ser_criado_com_sucesso_quando_apenas_os_dados_essenciais_sao_enviados_para_o_model_documento(
    pessoa,
):
    """Um documento deve ser criado com sucesso quando apenas os dados essenciais são enviados para o model Documento."""

    Documento.objects.create(pessoa=pessoa)
    assert Documento.objects.count() == 1


@pytest.mark.django_db
def test_um_documento_nao_deve_ser_criado_quando_o_campo_pessoa_nao_for_enviado_para_o_model_documento():
    """Um documento não deve ser criado quando o campo 'pessoa' não for enviado para o model Documento."""

    with pytest.raises(IntegrityError) as e:
        Documento.objects.create()

    assert "NOT NULL constraint failed: cadastros_documento.pessoa_id" == str(e.value)


@pytest.mark.django_db
@pytest.mark.parametrize("ModelClass, FactoryClass, name", PRINCIPAL_MODELS)
def test_o_primeiro_registro_criado_deve_ser_o_registro_principal_para_cada_pessoa(
    ModelClass, FactoryClass, name, pessoa_pf
):
    """Verifica se o primeiro registro de cada tipo se torna automaticamente principal."""
    registro = ModelClass.objects.create(pessoa=pessoa_pf)
    assert registro.e_principal


@pytest.mark.django_db
@pytest.mark.parametrize("ModelClass, FactoryClass, name", PRINCIPAL_MODELS)
def test_novo_registro_principal_desativa_o_antigo(ModelClass, FactoryClass, name, pessoa_pf):
    """Verifica se ao criar um novo principal, o antigo é desativado."""
    antigo = FactoryClass(pessoa=pessoa_pf, e_principal=True)

    ModelClass.objects.create(pessoa=pessoa_pf, e_principal=True)

    antigo.refresh_from_db()
    assert not antigo.e_principal


@pytest.mark.django_db
@pytest.mark.parametrize("ModelClass, FactoryClass, name", PRINCIPAL_MODELS)
def test_deve_haver_apenas_um_unico_registro_marcado_como_principal(ModelClass, FactoryClass, name, pessoa_pf):
    """Verifica se o sistema garante a unicidade do registro principal por pessoa."""

    FactoryClass.create_batch(5, pessoa=pessoa_pf, e_principal=True)
    assert ModelClass.objects.filter(pessoa=pessoa_pf, e_principal=True).count() == 1
