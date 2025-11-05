from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeSpampedModel(models.Model):
    criado = models.DateTimeField(_("Criado"), auto_now_add=True)
    modificado = models.DateTimeField(_("Modificado"), auto_now=True)

    class Meta:
        abstract = True
