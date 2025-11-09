from django.contrib import admin

from .models import (
    Banco,
    Documento,
    Email,
    Endereco,
    Pessoa,
    PessoaFisica,
    PessoaJuridica,
    Site,
    Telefone,
)


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    pass


@admin.register(PessoaFisica)
class PessoaFisicaAdmin(admin.ModelAdmin):
    pass


@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    pass


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    pass


@admin.register(Telefone)
class TelefoneAdmin(admin.ModelAdmin):
    pass


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    pass


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    pass


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    pass
