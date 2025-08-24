from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
from datetime import date

from djangosige import services
from djangosige.apps.financeiro.models import MovimentoCaixa


class QuantidadeCadastrosTests(TestCase):
    def test_quantidade_cadastros_counts_are_correct(self):
        with (
            patch(
                "djangosige.services.Cliente.objects"
            ) as MockClienteObjects,
            patch(
                "djangosige.services.Fornecedor.objects"
            ) as MockFornecedorObjects,
            patch(
                "djangosige.services.Produto.objects"
            ) as MockProdutoObjects,
            patch(
                "djangosige.services.Empresa.objects"
            ) as MockEmpresaObjects,
            patch(
                "djangosige.services.Transportadora.objects"
            ) as MockTransportadoraObjects,
        ):
            MockClienteObjects.count.return_value = 5
            MockFornecedorObjects.count.return_value = 3
            MockProdutoObjects.count.return_value = 10
            MockEmpresaObjects.count.return_value = 2
            MockTransportadoraObjects.count.return_value = 1

            result = services.quantidade_cadastros()
            self.assertEqual(
                result,
                {
                    "clientes": 5,
                    "fornecedores": 3,
                    "produtos": 10,
                    "empresas": 2,
                    "transportadoras": 1,
                },
            )

    def test_quantidade_cadastros_zero_counts(self):
        with (
            patch("djangosige.services.Cliente.objects") as MockCliente,
            patch("djangosige.services.Fornecedor.objects") as MockFornecedor,
            patch("djangosige.services.Produto.objects") as MockProduto,
            patch("djangosige.services.Empresa.objects") as MockEmpresa,
            patch(
                "djangosige.services.Transportadora.objects"
            ) as MockTransportadora,
        ):
            MockCliente.count.return_value = 0
            MockFornecedor.count.return_value = 0
            MockProduto.count.return_value = 0
            MockEmpresa.count.return_value = 0
            MockTransportadora.count.return_value = 0

            result = services.quantidade_cadastros()
            self.assertEqual(
                result,
                {
                    "clientes": 0,
                    "fornecedores": 0,
                    "produtos": 0,
                    "empresas": 0,
                    "transportadoras": 0,
                },
            )


class AgendaDoDiaTests(TestCase):
    @patch("djangosige.services.OrcamentoVenda")
    @patch("djangosige.services.OrcamentoCompra")
    @patch("djangosige.services.PedidoVenda")
    @patch("djangosige.services.PedidoCompra")
    @patch("djangosige.services.Entrada")
    @patch("djangosige.services.Saida")
    def test_contagem_agenda_do_dia_esta_correto(
        self,
        MockSaida,
        MockEntrada,
        MockPedidoCompra,
        MockPedidoVenda,
        MockOrcamentoCompra,
        MockOrcamentoVenda,
    ):
        test_date = date(2024, 6, 1)
        MockOrcamentoVenda.objects.filter.return_value.count.return_value = 7
        MockOrcamentoCompra.objects.filter.return_value.count.return_value = 4
        MockPedidoVenda.objects.filter.return_value.count.return_value = 3
        MockPedidoCompra.objects.filter.return_value.count.return_value = 2
        MockEntrada.objects.filter.return_value.count.return_value = 5
        MockSaida.objects.filter.return_value.count.return_value = 6

        result = services.agenda_do_dia(test_date)
        self.assertEqual(
            result,
            {
                "orcamento_venda_hoje": 7,
                "orcamento_compra_hoje": 4,
                "pedido_venda_hoje": 3,
                "pedido_compra_hoje": 2,
                "contas_receber_hoje": 5,
                "contas_pagar_hoje": 6,
            },
        )

    @patch("djangosige.services.OrcamentoVenda")
    @patch("djangosige.services.OrcamentoCompra")
    @patch("djangosige.services.PedidoVenda")
    @patch("djangosige.services.PedidoCompra")
    @patch("djangosige.services.Entrada")
    @patch("djangosige.services.Saida")
    def test_agenda_do_dia_zero_counts(
        self,
        MockSaida,
        MockEntrada,
        MockPedidoCompra,
        MockPedidoVenda,
        MockOrcamentoCompra,
        MockOrcamentoVenda,
    ):
        test_date = date(2024, 6, 1)
        MockOrcamentoVenda.objects.filter.return_value.count.return_value = 0
        MockOrcamentoCompra.objects.filter.return_value.count.return_value = 0
        MockPedidoVenda.objects.filter.return_value.count.return_value = 0
        MockPedidoCompra.objects.filter.return_value.count.return_value = 0
        MockEntrada.objects.filter.return_value.count.return_value = 0
        MockSaida.objects.filter.return_value.count.return_value = 0

        result = services.agenda_do_dia(test_date)
        self.assertEqual(
            result,
            {
                "orcamento_venda_hoje": 0,
                "orcamento_compra_hoje": 0,
                "pedido_venda_hoje": 0,
                "pedido_compra_hoje": 0,
                "contas_receber_hoje": 0,
                "contas_pagar_hoje": 0,
            },
        )


class AlertasTests(TestCase):
    @patch("djangosige.services.Produto")
    @patch("djangosige.services.OrcamentoVenda")
    @patch("djangosige.services.PedidoVenda")
    @patch("djangosige.services.OrcamentoCompra")
    @patch("djangosige.services.PedidoCompra")
    @patch("djangosige.services.Entrada")
    @patch("djangosige.services.Saida")
    def test_alertas_counts_are_correct(
        self,
        MockSaida,
        MockEntrada,
        MockPedidoCompra,
        MockOrcamentoCompra,
        MockPedidoVenda,
        MockOrcamentoVenda,
        MockProduto,
    ):
        test_date = date(2024, 6, 1)
        MockProduto.objects.filter.return_value.count.return_value = 2
        MockOrcamentoVenda.objects.filter.return_value.count.return_value = 3
        MockPedidoVenda.objects.filter.return_value.count.return_value = 4
        MockOrcamentoCompra.objects.filter.return_value.count.return_value = 5
        MockPedidoCompra.objects.filter.return_value.count.return_value = 6
        MockEntrada.objects.filter.return_value.count.return_value = 7
        MockSaida.objects.filter.return_value.count.return_value = 8

        result = services.alertas(test_date)
        self.assertEqual(
            result,
            {
                "produtos_baixo_estoque": 2,
                "orcamentos_venda_vencidos": 3,
                "pedidos_venda_atrasados": 4,
                "orcamentos_compra_vencidos": 5,
                "pedidos_compra_atrasados": 6,
                "contas_receber_atrasadas": 7,
                "contas_pagar_atrasadas": 8,
            },
        )

    @patch("djangosige.services.Produto")
    @patch("djangosige.services.OrcamentoVenda")
    @patch("djangosige.services.PedidoVenda")
    @patch("djangosige.services.OrcamentoCompra")
    @patch("djangosige.services.PedidoCompra")
    @patch("djangosige.services.Entrada")
    @patch("djangosige.services.Saida")
    def test_alertas_zero_counts(
        self,
        MockSaida,
        MockEntrada,
        MockPedidoCompra,
        MockOrcamentoCompra,
        MockPedidoVenda,
        MockOrcamentoVenda,
        MockProduto,
    ):
        test_date = date(2024, 6, 1)
        MockProduto.objects.filter.return_value.count.return_value = 0
        MockOrcamentoVenda.objects.filter.return_value.count.return_value = 0
        MockPedidoVenda.objects.filter.return_value.count.return_value = 0
        MockOrcamentoCompra.objects.filter.return_value.count.return_value = 0
        MockPedidoCompra.objects.filter.return_value.count.return_value = 0
        MockEntrada.objects.filter.return_value.count.return_value = 0
        MockSaida.objects.filter.return_value.count.return_value = 0

        result = services.alertas(test_date)
        self.assertEqual(
            result,
            {
                "produtos_baixo_estoque": 0,
                "orcamentos_venda_vencidos": 0,
                "pedidos_venda_atrasados": 0,
                "orcamentos_compra_vencidos": 0,
                "pedidos_compra_atrasados": 0,
                "contas_receber_atrasadas": 0,
                "contas_pagar_atrasadas": 0,
            },
        )


class MovimentoCaixaTests(TestCase):
    @patch("djangosige.services.MovimentoCaixa.objects")
    def test_movimento_caixa_found(self, mock_objects):
        test_date = date(2024, 6, 1)
        mock_instance = MagicMock()
        mock_objects.get.return_value = mock_instance

        result = services.movimento_caixa(test_date)

        expected = {"movimento_caixa": mock_instance}
        self.assertEqual(result, expected)
        mock_objects.get.assert_called_once_with(data_movimento=test_date)
        # Não deve chamar filter se encontrou o movimento
        mock_objects.filter.assert_not_called()

    @patch("djangosige.services.MovimentoCaixa.objects")
    def test_movimento_caixa_not_found_with_previous(self, mock_objects):
        test_date = date(2024, 6, 1)

        # Mock para quando não encontra movimento na data atual
        mock_objects.get.side_effect = MovimentoCaixa.DoesNotExist

        # Mock para filter().latest() - encontra movimento anterior
        mock_ultima_movimentacao = MagicMock()
        mock_ultima_movimentacao.saldo_final = 123.45

        # Configurar encadeamento: filter().latest()
        mock_objects.filter.return_value = mock_objects  # permite encadeamento
        mock_objects.latest.return_value = mock_ultima_movimentacao

        result = services.movimento_caixa(test_date)

        expected = {"saldo": 123.45}
        self.assertEqual(result, expected)
        mock_objects.get.assert_called_once_with(data_movimento=test_date)
        mock_objects.filter.assert_called_once_with(data_movimento__lt=test_date)
        mock_objects.latest.assert_called_once_with("data_movimento")

    @patch("djangosige.services.MovimentoCaixa.objects")
    def test_movimento_caixa_not_found_no_previous(self, mock_objects):
        test_date = date(2024, 6, 1)

        # Mock para quando não encontra movimento na data atual
        mock_objects.get.side_effect = MovimentoCaixa.DoesNotExist

        # Mock para quando não encontra movimento anterior
        mock_objects.filter.return_value = mock_objects  # permite encadeamento
        mock_objects.latest.side_effect = MovimentoCaixa.DoesNotExist

        result = services.movimento_caixa(test_date)

        expected = {"saldo": "0.00"}
        self.assertEqual(result, expected)
        mock_objects.get.assert_called_once_with(data_movimento=test_date)
        mock_objects.filter.assert_called_once_with(data_movimento__lt=test_date)
        mock_objects.latest.assert_called_once_with("data_movimento")
