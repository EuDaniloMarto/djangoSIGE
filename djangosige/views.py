from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def hadle404(request: HttpRequest) -> HttpResponse:
    return render(request, "404.html", status=HTTPStatus.NOT_FOUND)


def handle500(request: HttpRequest) -> HttpResponse:
    return render(request, "500.html", status=HTTPStatus.INTERNAL_SERVER_ERROR)
