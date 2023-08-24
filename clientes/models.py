from cpf_field.models import *
from cpf_field.models import CPFField
from django.db import models
import random


# ---------------------Cadastros primários------------------------
class PecasVeiculo(models.Model):
    pecas_veiculo = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Cadastro de Peças"

    def __str__(self):
        return self.pecas_veiculo


class TipoVeiculo(models.Model):
    tipoVeiculo = models.CharField(max_length=20, verbose_name="Tipo de veículo")

    class Meta:
        verbose_name_plural = "Cadastro de Veículo"

    def __str__(self):
        return self.tipoVeiculo


# -------------------------Cadastro de grupo----------------

class GrupoPecas(models.Model):
    grupo_pecas = models.CharField(max_length=20, verbose_name="Nome do Grupo")
    grupo_description = models.TextField(blank=True, null=False, verbose_name="Descrição do grupo cadastrado")
    pecas_veiculo = models.ManyToManyField(PecasVeiculo, verbose_name="Peças a serem adicionadas")

    class Meta:
        verbose_name_plural = "Cadastro de Grupo de Peças"

    def __str__(self):
        return self.grupo_pecas


# ----------------------------Clientes------------------------------------
class Cliente(models.Model):
    cliente_nome = models.CharField(max_length=100, verbose_name='Nome')
    cliente_email = models.EmailField(blank=False, null=False, verbose_name='Email')
    cliente_phone = models.CharField(max_length=20, blank=False, null=False, verbose_name="Telefone")
    cliente_cpf = CPFField('CPF', null=False, blank=False)
    cliente_endereco = models.CharField(max_length=100, blank=False, null=False, verbose_name="Endereço")

    class Meta:
        verbose_name_plural = "Cadastro de Cliente"

    def __str__(self):
        return self.cliente_nome


# -----------------------Veículos--------------------

class Veiculo(models.Model):
    veiculo_tipo = models.ForeignKey(TipoVeiculo, on_delete=models.CASCADE)
    veiculo_data = models.DateField(auto_now_add=True, blank=False, null=True, verbose_name="Data de Cadastro")
    veiculo_placa = models.CharField(max_length=10, verbose_name="Placa do veículo", unique=True)
    veiculo_operante = models.BooleanField(default=False, blank=False, null=False)
    veiculo_descricao = models.TextField(blank=True, null=False, verbose_name='Descrição do Veículo')
    veiculo_grupo_pecas = models.ForeignKey(GrupoPecas, on_delete=models.CASCADE,
                                            verbose_name='Grupo de peças associado', null=True)
    veiculo_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')

    class Meta:
        verbose_name_plural = "Veículo"

    def __str__(self):
        return self.veiculo_placa


# -----------------------Ordem de serviço--------------------

from django.db import models


class OrdemServico(models.Model):
    ordem_codigo = models.IntegerField(verbose_name='Código', unique=True, editable=False)
    ordem_placa = models.ForeignKey(
        Veiculo,
        to_field='veiculo_placa',
        verbose_name="Placa do veículo",
        on_delete=models.CASCADE
    )
    ordem_cliente = models.ForeignKey(
        Cliente,
        verbose_name="Cliente associado",
        on_delete=models.CASCADE
    )
    ordem_data = models.DateField(
        auto_now_add=True,
        blank=False,
        null=True,
        verbose_name="Data de Cadastro"
    )
    ordem_data_atualizada = models.DateTimeField(
        auto_now=True,
        blank=False,
        null=False,
        verbose_name="Última atualização"
    )
    ordem_classificacao = models.BooleanField(
        default=False,
        blank=False,
        null=False,
        verbose_name="Ordem aberta?"
    )
    ordem_descricao = models.TextField(
        blank=True,
        null=False,
        verbose_name='Descrição do procedimento'
    )
    ordem_grupo_pecas = models.ForeignKey(
        GrupoPecas,
        on_delete=models.CASCADE,
        verbose_name="Grupo de peças",
        null=True,
        blank=True
    )
    ordem_troca = models.BooleanField(
        default=False,
        blank=False,
        null=False,
        verbose_name="Troca de peça?"
    )
    ordem_valor_servico = models.IntegerField(
        default=0,
        verbose_name='Valor do serviço'
    )
    ordem_peca = models.IntegerField(
        default=0,
        verbose_name='Valor da peça'
    )
    pecas_grupo = models.ManyToManyField(
        PecasVeiculo,
        blank=True,
        verbose_name="Peças do Grupo"
    )
    ordem_valor = models.IntegerField(
        default=0,
        verbose_name='Outros Gastos'
    )
    ordem_outros = models.TextField(
        max_length=40,
        blank=True,
        null=False,
        verbose_name='Descrição dos gastos'
    )

    class Meta:
        verbose_name_plural = "Ordens de Serviço"

    def __str__(self):
        return str(self.ordem_codigo)

    def save(self, *args, **kwargs):
        if not self.ordem_codigo:
            while True:
                codigo = random.randint(10000, 99999)
                if not OrdemServico.objects.filter(ordem_codigo=codigo).exists():
                    self.ordem_codigo = codigo
                    break

        super().save(*args, **kwargs)

        if self.ordem_grupo_pecas:
            self.pecas_grupo.set(self.ordem_grupo_pecas.pecas_veiculo.all())
        else:
            self.pecas_grupo.clear()
