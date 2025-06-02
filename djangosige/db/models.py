from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    criado_em = models.DateTimeField(_("Criado em"), auto_now_add=True)
    atualizado_em = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        abstract = True
