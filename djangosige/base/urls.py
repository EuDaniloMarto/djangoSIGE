# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

from django.conf import settings

app_name = 'base'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', views.handler404),
        url(r'^500/$', views.handler500),
    ]
