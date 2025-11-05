from django.contrib import admin

from .models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = (
        "descricao",
        "tipo_pessoa",
        "eh_cliente",
        "eh_fornecedor",
        "eh_transportadora",
    )
    list_filter = ("tipo_pessoa", "eh_cliente", "eh_fornecedor", "eh_transportadora")
    list_editable = ("eh_cliente", "eh_fornecedor", "eh_transportadora")
    search_fields = ("descricao",)
