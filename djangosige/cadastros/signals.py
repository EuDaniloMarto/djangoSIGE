from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    Banco,
    Email,
    Endereco,
    Pessoa,
    PessoaFisica,
    PessoaJuridica,
    Site,
    Telefone,
)


@receiver(post_save, sender=Pessoa)
def criar_registros_iniciais_para_pessoa(sender, instance, created, **kwargs):
    """
    Cria automaticamente os registros iniciais em PessoaFisica/Juridica
    e os registros principais para Endereco, Telefone, Email, Site e Banco.
    """
    if created:
        if instance.tipo_pessoa == Pessoa.EscolherTipoPessoa.PF:
            PessoaFisica.objects.get_or_create(pessoa=instance)

        elif instance.tipo_pessoa == Pessoa.EscolherTipoPessoa.PJ:
            PessoaJuridica.objects.get_or_create(pessoa=instance)

        Endereco.objects.get_or_create(pessoa=instance)
        Telefone.objects.get_or_create(pessoa=instance)
        Email.objects.get_or_create(pessoa=instance)
        Site.objects.get_or_create(pessoa=instance)
        Banco.objects.get_or_create(pessoa=instance)
