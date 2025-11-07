from django.test import SimpleTestCase, RequestFactory
from django.core.paginator import Paginator
from djangosige.templatetags.djangosige import paginacao


class TestPaginacaoTag(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def make_context(self, query_params=None):
        request = self.factory.get("/", data=query_params or {})
        return {"request": request}

    def make_page_obj(self, total_items=100, per_page=10, page=5):
        paginator = Paginator(range(total_items), per_page)
        return paginator.page(page)

    def test_contexto_basico_retorna_chaves_esperadas(self):
        page_obj = self.make_page_obj()
        context = self.make_context()
        result = paginacao(context, page_obj)
        self.assertIn("pages", result)
        self.assertIn("base_url", result)
        self.assertIn("page_obj", result)

    def test_total_de_paginas_menor_que_7_mostra_todas_sem_elipses(self):
        page_obj = self.make_page_obj(total_items=30, per_page=5, page=1)  # 6 páginas
        result = paginacao(self.make_context(), page_obj)
        self.assertEqual(result["pages"], [1, 2, 3, 4, 5, 6])
        self.assertNotIn("...", result["pages"])

    def test_total_grande_adiciona_elipses(self):
        page_obj = self.make_page_obj(total_items=1000, per_page=10, page=50)
        result = paginacao(self.make_context(), page_obj)
        self.assertIn("...", result["pages"])
        self.assertIn(1, result["pages"])
        self.assertIn(100, result["pages"])

    def test_paginas_vizinhas_sao_exibidas_ao_redor_da_atual(self):
        page_obj = self.make_page_obj(total_items=100, per_page=1, page=10)
        result = paginacao(self.make_context(), page_obj)
        # Deve mostrar páginas de 8 a 12 (±2 em torno de 10)
        vizinhos = list(range(8, 13))
        for v in vizinhos:
            self.assertIn(v, result["pages"])

    def test_preserva_parametros_GET_na_base_url(self):
        context = self.make_context({"busca": "django", "ativo": "1"})
        page_obj = self.make_page_obj(page=3)
        result = paginacao(context, page_obj)
        base_url = result["base_url"]
        self.assertIn("?busca=django", base_url)
        self.assertIn("ativo=1", base_url)
        self.assertIn("&page=", base_url)

    def test_remove_parametro_de_paginacao_existente_dos_GET(self):
        context = self.make_context({"page": "4", "busca": "teste"})
        page_obj = self.make_page_obj(page=2)
        result = paginacao(context, page_obj)
        self.assertNotIn("page=4", result["base_url"])
        self.assertIn("busca=teste", result["base_url"])

    def test_base_url_sem_parametros_GET(self):
        context = self.make_context()
        page_obj = self.make_page_obj(page=1)
        result = paginacao(context, page_obj)
        self.assertEqual(result["base_url"], "?page=")

    def test_funciona_mesmo_sem_request_no_context(self):
        page_obj = self.make_page_obj(page=1)
        context = {}  # sem request
        result = paginacao(context, page_obj)
        self.assertEqual(result["base_url"], "?page=")

    def test_usa_parametro_customizado_param_name(self):
        page_obj = self.make_page_obj(page=1)
        result = paginacao(self.make_context(), page_obj, param_name="pagina")
        self.assertEqual(result["base_url"], "?pagina=")
