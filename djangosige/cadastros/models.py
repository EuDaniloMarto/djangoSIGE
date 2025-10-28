from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from djangosige.models import TimeStampedModel


class Cadastro(TimeStampedModel):
    class TipoCadastro(models.TextChoices):
        PF = "PF", _("Pessoa Física")
        PJ = "PJ", _("Pessoa Jurídica")

    colaborador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Colaborador"),
        on_delete=models.PROTECT,
    )
    descricao = models.CharField(_("Descrição"), max_length=255, unique=True)
    tipo_cadastros = models.CharField(
        _("Tipo de cadastros"),
        max_length=2,
        choices=TipoCadastro.choices,
        default=TipoCadastro.PF,
    )
    eh_cliente = models.BooleanField(_("É Cliente"), default=False)
    eh_fornecedora = models.BooleanField(_("É Fornecedor"), default=False)
    eh_transportadora = models.BooleanField(_("É Transportadora"), default=False)
    ativo = models.BooleanField(_("Ativo"), default=True)
    observacoes = models.TextField(_("Observações"), blank=True)

    class Meta:
        ordering = ("descricao",)
        verbose_name = _("Cadastro")
        verbose_name_plural = _("Cadastros")

    def __str__(self):
        return str(self.descricao)

    def get_absolute_url(self):
        return reverse("cadastros:ver_cadastro", kwargs={"pk": self.pk})
