from django.contrib import admin

from .models import Cadastro


@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin):
    list_display = (
        "descricao",
        "tipo_cadastros",
        "eh_cliente",
        "eh_fornecedora",
        "eh_transportadora",
    )
    list_editable = (
        "tipo_cadastros",
        "eh_cliente",
        "eh_fornecedora",
        "eh_transportadora",
    )
    search_fields = ("descricao",)
