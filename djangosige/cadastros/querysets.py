from django.db import models


class PessoaQuerySet(models.QuerySet):
    def clientes(self):
        return self.filter(e_cliente=True)

    def fornecedores(self):
        return self.filter(e_fornecedor=True)

    def transportadoras(self):
        return self.filter(e_transportadora=True)

    def ativos(self):
        return self.filter(esta_ativo=True)
