from http import HTTPStatus

from django.test import TestCase
from django.test.client import RequestFactory

from djangosige.views import handle500


class TestCaseHandle404(TestCase):
    def test_404(self):
        response = self.client.get("/pg_nao_existe")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestCaseHandle500(TestCase):
    def test_handler500(self):
        factory = RequestFactory()
        request = factory.get("/")
        response = handle500(request)
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn("500", response.content.decode().lower())
