"""
Este módulo fornece serviços utilitários para o sistema, incluindo funções para contagem de registros principais,
resumo da agenda diária, geração de alertas comerciais e recuperação da movimentação de caixa.

Funções:
- quantidade_cadastros(): Retorna a contagem total de registros para entidades principais (clientes, fornecedores, produtos, empresas, transportadoras).
- agenda_do_dia(data_atual): Retorna um resumo da agenda do dia, incluindo orçamentos, pedidos e contas a receber/pagar para a data informada.
- alertas(data_atual): Gera contagens de alertas para produtos com baixo estoque, orçamentos/pedidos vencidos ou atrasados, e contas a receber/pagar em atraso.
- movimento_caixa(data_atual): Recupera informações da movimentação de caixa para uma data específica, incluindo saldo e movimentação diária.

Dependências:
- Modelos Django das apps: cadastro, vendas, compras, financeiro.
"""

from django.db.models import F

from djangosige.apps.cadastro.models import (
    Cliente,
    Empresa,
    Fornecedor,
    Produto,
    Transportadora,
)
from djangosige.apps.compras.models import OrcamentoCompra, PedidoCompra
from djangosige.apps.financeiro.models import Entrada, MovimentoCaixa, Saida
from djangosige.apps.vendas.models import OrcamentoVenda, PedidoVenda


def quantidade_cadastros():
    """
    Retorna um dicionário contendo a contagem total de registros para cada entidade principal no sistema.

    As chaves do dicionário representam os nomes das entidades:
    - 'clientes': Número total de registros de Clientes.
    - 'fornecedores': Número total de registros de Fornecedores.
    - 'produtos': Número total de registros de Produto.
    - 'empresas': Número total de registros de Empresas.
    - 'transportadoras': Número total de registros de Transportadoras.

    Retorna:
    dict: Um mapeamento de nomes de entidades para suas respectivas contagens de registros.
    """
    return {
        "clientes": Cliente.objects.count(),
        "fornecedores": Fornecedor.objects.count(),
        "produtos": Produto.objects.count(),
        "empresas": Empresa.objects.count(),
        "transportadoras": Transportadora.objects.count(),
    }


def agenda_do_dia(data_atual):
    """
    Retorna um resumo da agenda de hoje, incluindo contagens de orçamentos de vendas e compras, pedidos e contas a receber/pagar para a data informada.

    Argumentos:
    data_atual (data): A data para a qual o resumo da agenda deve ser recuperado.

    Retorna:
    dict: Um dicionário contendo as seguintes chaves:
    - "orcamento_venda_hoje": Contagem de orçamentos de vendas com vencimento hoje com status "0".
    - "orcamento_compra_hoje": Contagem de orçamentos de compras com vencimento hoje com status "0".
    - "pedido_venda_hoje": Contagem de pedidos de vendas a serem entregues hoje com status "0".
    - "pedido_compra_hoje": Contagem de pedidos de compras a serem entregues hoje com status "0".
    - "contas_receber_hoje": Contagem de lançamentos a receber com vencimento hoje com status "1" ou "2".

    - "contas_pagar_hoje": Contagem de lançamentos a pagar com vencimento hoje com status "1" ou "2".
    """

    return {
        "orcamento_venda_hoje": OrcamentoVenda.objects.filter(
            data_vencimento=data_atual, status="0"
        ).count(),
        "orcamento_compra_hoje": OrcamentoCompra.objects.filter(
            data_vencimento=data_atual, status="0"
        ).count(),
        "pedido_venda_hoje": PedidoVenda.objects.filter(
            data_entrega=data_atual, status="0"
        ).count(),
        "pedido_compra_hoje": PedidoCompra.objects.filter(
            data_entrega=data_atual, status="0"
        ).count(),
        "contas_receber_hoje": Entrada.objects.filter(
            data_vencimento=data_atual, status__in=["1", "2"]
        ).count(),
        "contas_pagar_hoje": Saida.objects.filter(
            data_vencimento=data_atual, status__in=["1", "2"]
        ).count(),
    }

def alertas(data_atual):
    """
    Gera um dicionário de contagens de alertas para diversas entidades comerciais com base na data atual.

    Argumentos:
    data_atual (datetime.date ou datetime.datetime): A data atual para comparação com as datas de vencimento e de entrega.

    Retorna:
    dict: Um dicionário contendo as seguintes chaves e suas respectivas contagens:
    - "produtos_baixo_estoque": Quantidade de produtos com estoque atual menor ou igual ao estoque mínimo.
    - "orcamentos_venda_vencidos": Quantidade de cotações de venda vencidas e com status "0".
    - "pedidos_venda_atrasados": Quantidade de pedidos de venda atrasados ​​(data de entrega já passada) e com status "0".
    - "orcamentos_compra_vencidos": Quantidade de cotações de compra vencidas e com status "0".
    - "pedidos_compra_atrasados": Quantidade de pedidos de compra atrasados ​​(data de entrega já passada) e com status "0".

    - "contas_receber_atrasadas": Quantidade de lançamentos de contas a receber em atraso e com status "1" ou "2".
    - "contas_pagar_atrasadas": Quantidade de lançamentos de contas a pagar em atraso e com status "1" ou "2".
    """

    return {
        "produtos_baixo_estoque": Produto.objects.filter(
            estoque_atual__lte=F("estoque_minimo")
        ).count(),
        "orcamentos_venda_vencidos": OrcamentoVenda.objects.filter(
            data_vencimento__lte=data_atual, status="0"
        ).count(),
        "pedidos_venda_atrasados": PedidoVenda.objects.filter(
            data_entrega__lte=data_atual, status="0"
        ).count(),
        "orcamentos_compra_vencidos": OrcamentoCompra.objects.filter(
            data_vencimento__lte=data_atual, status="0"
        ).count(),
        "pedidos_compra_atrasados": PedidoCompra.objects.filter(
            data_entrega__lte=data_atual, status="0"
        ).count(),
        "contas_receber_atrasadas": Entrada.objects.filter(
            data_vencimento__lte=data_atual, status__in=["1", "2"]
        ).count(),
        "contas_pagar_atrasadas": Saida.objects.filter(
            data_vencimento__lte=data_atual, status__in=["1", "2"]
        ).count(),
    }


def movimento_caixa(data_atual):
    """
    Recupera a movimentação de caixa para uma determinada data.

    Argumentos:
    data_atual (data): A data para a qual a movimentação de caixa deve ser recuperada.

    Retorna:
    dict: Um dicionário contendo informações sobre a movimentação de caixa para a data especificada.
    Chaves:
    - "movimento_dia": Espaço reservado para movimentação diária (string).
    - "caixa": Espaço reservado para valor em dinheiro (string, padrão "0,00").
    - "movimento_caixa": Instância de MovimentoCaixa para a data fornecida, se encontrada.
    - "saldo": Saldo final da última movimentação anterior, se não houver movimentação para a data fornecida.
    """

    caixa = {}

    try:
        caixa["movimento_caixa"] = MovimentoCaixa.objects.get(data_movimento=data_atual)
    except MovimentoCaixa.DoesNotExist:
        try:
            ultima_movimentacao = MovimentoCaixa.objects.filter(
                data_movimento__lt=data_atual
            ).latest("data_movimento")
            caixa["saldo"] = ultima_movimentacao.saldo_final
        except MovimentoCaixa.DoesNotExist:
            caixa["saldo"] = "0.00"

    return caixa
