from django.db.models import F

from cadastro.models import Cliente, Empresa, Fornecedor, Produto, Transportadora
from compras.models import OrcamentoCompra, PedidoCompra
from vendas.models import OrcamentoVenda, PedidoVenda
from financeiro.models import Entrada, MovimentoCaixa, Saida


def quantidade_clientes():
    """Retorna a contagem total de clientes."""
    return Cliente.objects.all().count()


def quantidade_fornecedores():
    """Retorna a contagem total de fornecedores."""
    return Fornecedor.objects.all().count()


def quantidade_transportadoras():
    """Retorna a contagem total de transportadoras."""
    return Transportadora.objects.all().count()


def quantidade_empresas():
    """Retorna a contagem total de empresas."""
    return Empresa.objects.all().count()


def quantidade_produtos():
    """Retorna a contagem total de produtos."""
    return Produto.objects.all().count()


def orcamento_venda(hoje):
    """Retorna a contagem de orçamentos de venda não finalizados para hoje."""
    return OrcamentoVenda.objects.filter(data_vencimento=hoje, status='0').count()


def orcamento_compra(hoje):
    """Retorna a contagem de orçamentos de compra não finalizados para hoje."""
    return OrcamentoCompra.objects.filter(data_vencimento=hoje, status='0').count()


def pedido_venda(hoje):
    """Retorna a contagem de pedidos de venda não finalizados para hoje."""
    return PedidoVenda.objects.filter(data_entrega=hoje, status='0').count()


def pedido_compra(hoje):
    """Retorna a contagem de pedidos de compra não finalizados para hoje."""
    return PedidoCompra.objects.filter(data_entrega=hoje, status='0').count()


def contas_receber(hoje):
    """Retorna a contagem de contas a receber pendentes ou parcialmente pagas para hoje."""
    return Entrada.objects.filter(data_vencimento=hoje, status__in=['1', '2']).count()


def contas_pagar(hoje):
    """Retorna a contagem de contas a pagar pendentes ou parcialmente pagas para hoje."""
    return Saida.objects.filter(data_vencimento=hoje, status__in=['1', '2']).count()


def produtos_baixo_estoque():
    """Retorna a contagem de produtos com estoque abaixo do mínimo."""
    return Produto.objects.filter(estoque_atual__lte=F('estoque_minimo')).count()


def orcamentos_venda_vencidos(hoje):
    """Retorna a contagem de orçamentos de venda vencidos e não finalizados."""
    return OrcamentoVenda.objects.filter(data_vencimento__lte=hoje, status='0').count()


def pedidos_venda_atrasados(hoje):
    """Retorna a contagem de pedidos de venda atrasados e não finalizados."""
    return PedidoVenda.objects.filter(data_entrega__lte=hoje, status='0').count()


def orcamentos_compra_vencidos(hoje):
    """Retorna a contagem de orçamentos de compra vencidos e não finalizados."""
    return OrcamentoCompra.objects.filter(data_vencimento__lte=hoje, status='0').count()


def pedidos_compra_atrasados(hoje):
    """Retorna a contagem de pedidos de compra atrasados e não finalizados."""
    return PedidoCompra.objects.filter(data_entrega__lte=hoje, status='0').count()


def contas_receber_atrasadas(hoje):
    """Retorna a contagem de contas a receber atrasadas e pendentes/parcialmente pagas."""
    return Entrada.objects.filter(data_vencimento__lte=hoje, status__in=['1', '2']).count()


def contas_pagar_atrasadas(hoje):
    """Retorna a contagem de contas a pagar atrasadas e pendentes/parcialmente pagas."""
    return Saida.objects.filter(data_vencimento__lte=hoje, status__in=['1', '2']).count()


def get_quantidade_cadastro():
    """Agrupa as contagens de diferentes tipos de cadastro."""
    return {
        'clientes': quantidade_clientes(),
        'fornecedores': quantidade_fornecedores(),
        'transportadoras': quantidade_transportadoras(),
        'empresas': quantidade_empresas(),
        'produtos': quantidade_produtos(),
    }


def get_agenda_hoje(hoje):
    """Agrupa os itens da agenda para o dia atual."""
    return {
        'orcamento_venda_hoje': orcamento_venda(hoje),
        'orcamento_compra_hoje': orcamento_compra(hoje),
        'pedido_venda_hoje': pedido_venda(hoje),
        'pedido_compra_hoje': pedido_compra(hoje),
        'contas_receber_hoje': contas_receber(hoje),
        'contas_pagar_hoje': contas_pagar(hoje),
    }


def get_alertas(hoje):
    """Agrupa os diferentes tipos de alertas."""
    return {
        'produtos_baixo_estoque': produtos_baixo_estoque(),
        'orcamentos_venda_vencidos': orcamentos_venda_vencidos(hoje),
        'pedidos_venda_atrasados': pedidos_venda_atrasados(hoje),
        'orcamentos_compra_vencidos': orcamentos_compra_vencidos(hoje),
        'pedidos_compra_atrasados': pedidos_compra_atrasados(hoje),
        'contas_receber_atrasadas': contas_receber_atrasadas(hoje),
        'contas_pagar_atrasadas': contas_pagar_atrasadas(hoje),
    }


def get_movimento_e_saldo(hoje):
    """Busca o movimento de caixa do dia e calcula o saldo."""
    movimento_dia = MovimentoCaixa.objects.filter(data_movimento=hoje).first()
    saldo = '0,00'

    if movimento_dia:
        saldo = movimento_dia.saldo_final
    else:
        ultimo_mvmt = MovimentoCaixa.objects.filter(data_movimento__lt=hoje).order_by('-data_movimento').first()
        saldo = ultimo_mvmt.saldo_final if ultimo_mvmt else '0,00'

    return {
        'movimento_dia': movimento_dia,
        'saldo': saldo,
    }
