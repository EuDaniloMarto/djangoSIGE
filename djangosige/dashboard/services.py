from datetime import date
from typing import Dict

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from djangosige.cadastro.models import (
    Cliente,
    Empresa,
    Fornecedor,
    Produto,
    Transportadora,
)
from djangosige.compras.models import OrcamentoCompra, PedidoCompra
from djangosige.financeiro.models import Entrada, MovimentoCaixa, Saida
from djangosige.vendas.models import OrcamentoVenda, PedidoVenda


def quantidade_total_registros_entidades_principais() -> Dict[str, int]:
    return {
        "clientes": Cliente.objects.count(),
        "fornecedores": Fornecedor.objects.count(),
        "produtos": Produto.objects.count(),
        "empresas": Empresa.objects.count(),
        "transportadoras": Transportadora.objects.count(),
    }


def contagem_eventos_agendados_dia_hoje(data: date) -> Dict[str, int]:
    return {
        "orcamento_venda_hoje": OrcamentoVenda.objects.filter(
            data_vencimento=data, status="0"
        ).count(),
        "orcamento_compra_hoje": OrcamentoCompra.objects.filter(
            data_vencimento=data, status="0"
        ).count(),
        "pedido_venda_hoje": PedidoVenda.objects.filter(
            data_entrega=data, status="0"
        ).count(),
        "pedido_compra_hoje": PedidoCompra.objects.filter(
            data_entrega=data, status="0"
        ).count(),
        "contas_receber_hoje": Entrada.objects.filter(
            data_vencimento=data, status__in=["1", "2"]
        ).count(),
        "contas_pagar_hoje": Saida.objects.filter(
            data_vencimento=data, status__in=["1", "2"]
        ).count(),
    }


def situacoes_criticas_para_exibir_alertas_na_dashboard(data: date) -> Dict[str, int]:
    return {
        "produtos_baixo_estoque": Produto.objects.filter(
            estoque_atual__lte=F("estoque_minimo")
        ).count(),
        "orcamentos_venda_vencidos": OrcamentoVenda.objects.filter(
            data_vencimento__lt=data, status="0"
        ).count(),
        "pedidos_venda_atrasados": PedidoVenda.objects.filter(
            data_entrega__lt=data, status="0"
        ).count(),
        "orcamentos_compra_vencidos": OrcamentoCompra.objects.filter(
            data_vencimento__lt=data, status="0"
        ).count(),
        "pedidos_compra_atrasados": PedidoCompra.objects.filter(
            data_entrega__lt=data, status="0"
        ).count(),
        "contas_receber_atrasadas": Entrada.objects.filter(
            data_vencimento__lt=data, status__in=["1", "2"]
        ).count(),
        "contas_pagar_atrasadas": Saida.objects.filter(
            data_vencimento__lt=data, status__in=["1", "2"]
        ).count(),
    }


def movimento_caixa_hoje(data: date) -> Dict[str, int]:
    try:
        return {"movimento_dia": MovimentoCaixa.objects.get(data_movimento=data)}
    except ObjectDoesNotExist:
        ultimo = (
            MovimentoCaixa.objects.filter(data_movimento__lt=data)
            .order_by("-data_movimento")
            .first()
        )
        return {"saldo": ultimo.saldo_final if ultimo else "0,00"}
