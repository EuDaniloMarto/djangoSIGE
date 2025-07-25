from django.conf import settings
from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path('', views.pagina_inicial, name='index'),
]

if settings.DEBUG:
    urlpatterns = [
        *urlpatterns,
        path('404/', views.handler404),
        path('500/', views.handler500),
    ]
