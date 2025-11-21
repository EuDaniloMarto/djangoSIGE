from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .choices import EscolherBanco
from .querysets import PessoaQuerySet
from .validators import validate_cnpj, validate_cpf


class TimeStampedModel(models.Model):
    criado = models.DateTimeField(_("Criado"), auto_now_add=True)
    modificado = models.DateTimeField(_("Modificado"), auto_now=True)

    class Meta:
        abstract = True


class RegistroPrincipalPorPessoa(TimeStampedModel):
    pessoa = models.ForeignKey("cadastros.Pessoa", on_delete=models.CASCADE, verbose_name=_("Pessoa"))
    e_principal = models.BooleanField(_("É Padrão"), default=False)

    class Meta:
        ordering = ("pessoa",)
        abstract = True

    def __str__(self):
        return str(self.pessoa)

    def save(self, *args, **kwargs):
        ModelClass = self.__class__

        if self.pessoa_id:
            is_first_record = not ModelClass.objects.filter(pessoa=self.pessoa).exists()
            if is_first_record:
                self.e_principal = True
            elif not is_first_record and self.e_principal:
                ModelClass.objects.filter(pessoa=self.pessoa, e_principal=True).exclude(pk=self.pk).update(
                    e_principal=False
                )

        return super().save(*args, **kwargs)


class Pessoa(TimeStampedModel):
    class EscolherTipoPessoa(models.TextChoices):
        PF = "PF", _("Pessoa Física")
        PJ = "PJ", _("Pessoa Jurídica")

    colaborador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Colaborador"), related_name="pessoas"
    )
    descricao = models.CharField(
        _("Descrição"),
        max_length=255,
        unique=True,
        validators=[MinLengthValidator(1, _("Este campo não pode ser vazio."))],
    )
    tipo_pessoa = models.CharField(
        _("Tipo de Pessoa"), max_length=2, choices=EscolherTipoPessoa.choices, default=EscolherTipoPessoa.PF
    )
    e_cliente = models.BooleanField(_("É Cliente"), default=False)
    e_fornecedor = models.BooleanField(_("É Fornecedor"), default=False)
    e_transportadora = models.BooleanField(_("É Transportadora"), default=False)
    esta_ativo = models.BooleanField(_("Está ativo"), default=True)
    observacoes = models.TextField(_("Observações"), blank=True)
    objects = PessoaQuerySet.as_manager()

    class Meta:
        ordering = ("descricao",)
        verbose_name = _("Pessoa")
        verbose_name_plural = _("Pessoas")

    def __str__(self):
        return str(self.descricao)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cadastros:ver", kwargs={"pk": self.pk})

    def get_absolute_update_url(self):
        return reverse("cadastros:editar", kwargs={"pk": self.pk})


class PessoaFisica(TimeStampedModel):
    pessoa = models.OneToOneField("cadastros.Pessoa", on_delete=models.CASCADE, related_name="fisica")
    rg = models.CharField(_("RG"), max_length=16, blank=True)
    cpf = models.CharField(_("CPF"), max_length=11, blank=True, validators=[validate_cpf])
    nascimento = models.DateField(_("Data de Nascimento"), blank=True, null=True)

    class Meta:
        ordering = ("pessoa",)
        verbose_name = _("Pessoa Física")
        verbose_name_plural = _("Pessoas Físicas")

    def __str__(self):
        return str(self.pessoa)


class PessoaJuridica(TimeStampedModel):
    class EscolherEnquadramentoFiscal(models.TextChoices):
        LR = "LR", _("Lucro Real")
        LP = "LP", _("Lucro Presumido")
        SN = "SN", _("Simples Nacional")
        SE = "SE", _("Simples Nacional, excesso sublimite de receita bruta")

    pessoa = models.OneToOneField("cadastros.Pessoa", on_delete=models.CASCADE, related_name="juridica")
    nome_fantasia = models.CharField(_("Nome Fantasia"), max_length=36, blank=True)
    cnpj = models.CharField(_("CNPJ"), max_length=14, blank=True, validators=[validate_cnpj])
    inscricao_municipal = models.CharField(_("Inscrição Municipal"), max_length=36, blank=True)
    inscricao_estadual = models.CharField(_("Inscrição Estadual"), max_length=36, blank=True)
    proprietario = models.CharField(_("Proprietário"), max_length=64, blank=True)
    situacao_fiscal = models.CharField(
        _("Situação Fiscal"), max_length=2, choices=EscolherEnquadramentoFiscal.choices, blank=True, null=True
    )
    suframa = models.CharField(_("SUFRAMA"), max_length=16, blank=True)

    class Meta:
        ordering = ("pessoa",)
        verbose_name = _("Pessoa Jurídica")
        verbose_name_plural = _("Pessoas Jurídicas")

    def __str__(self):
        return str(self.pessoa)


class Endereco(RegistroPrincipalPorPessoa):
    logradouro = models.CharField(_("Logradouro"), max_length=255, blank=True)
    numero = models.CharField(_("Número"), max_length=16, blank=True)
    complemento = models.CharField(_("Complemento"), max_length=64, blank=True)
    bairro = models.CharField(_("Bairro"), max_length=64, blank=True)
    municipio = models.CharField(_("Município"), max_length=64, blank=True)
    uf = models.CharField(_("UF"), max_length=3, blank=True)
    pais = models.CharField(_("País"), max_length=32, blank=True, default="Brasil")
    cep = models.CharField(_("CEP"), max_length=16, blank=True)
    e_entrega = models.BooleanField(_("É entrega"), default=False)
    e_cobranca = models.BooleanField(_("É cobrança"), default=False)


class Telefone(RegistroPrincipalPorPessoa):
    telefone = models.CharField(_("Número"), max_length=32, blank=True)


class Email(RegistroPrincipalPorPessoa):
    email = models.EmailField(_("Email"), max_length=255, blank=True)


class Site(RegistroPrincipalPorPessoa):
    site = models.URLField(_("URL"), max_length=255, blank=True)


class Banco(RegistroPrincipalPorPessoa):
    banco = models.CharField(max_length=3, choices=EscolherBanco.choices, null=True, blank=True)
    agencia = models.CharField(max_length=8, null=True, blank=True)
    conta = models.CharField(max_length=32, null=True, blank=True)
    digito = models.CharField(max_length=8, null=True, blank=True)


class Documento(TimeStampedModel):
    pessoa = models.ForeignKey("cadastros.Pessoa", on_delete=models.CASCADE, verbose_name=_("Pessoa"))
    tipo = models.CharField(_("Tipo"), max_length=32, blank=True)
    documento = models.TextField(_("Documento"), blank=True)
