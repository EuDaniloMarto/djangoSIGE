"""djangosige URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangosige.apps.base.urls')),
    path('login/', include('djangosige.apps.login.urls')),
    path('cadastro/', include('djangosige.apps.cadastro.urls')),
    path('fiscal/', include('djangosige.apps.fiscal.urls')),
    path('vendas/', include('djangosige.apps.vendas.urls')),
    path('compras/', include('djangosige.apps.compras.urls')),
    path('financeiro/', include('djangosige.apps.financeiro.urls')),
    path('estoque/', include('djangosige.apps.estoque.urls')),
]

if settings.DEBUG is True:
    urlpatterns = [
        *urlpatterns,
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
