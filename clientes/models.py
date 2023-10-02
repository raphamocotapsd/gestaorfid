from django.db import models
import random
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('O CPF deve conter apenas números')


# ---------------------Cadastros primários------------------------
class PecasVeiculo(models.Model):
    pecas_veiculo = models.CharField(max_length=30, verbose_name="Peças do veículo")

    class Meta:
        verbose_name_plural = "02-Cadastro de Peças"

    def __str__(self):
        return self.pecas_veiculo


class TipoVeiculo(models.Model):
    tipoVeiculo = models.CharField(max_length=30, verbose_name="Tipo de veículo")

    class Meta:
        verbose_name_plural = "03-Cadastro de Veículo"

    def __str__(self):
        return self.tipoVeiculo


# -------------------------Cadastro de grupo----------------

class GrupoPecas(models.Model):
    grupo_pecas = models.CharField(max_length=30, verbose_name="Nome do conjunto")
    grupo_description = models.TextField(blank=True, null=False, verbose_name="Descrição do conjunto cadastrado")
    pecas_veiculo = models.ManyToManyField(PecasVeiculo, verbose_name="Peças a serem adicionadas")

    class Meta:
        verbose_name_plural = "04-Cadastro de Sistema"

    def __str__(self):
        return self.grupo_pecas


# ----------------------------Clientes------------------------------------
class Cliente(models.Model):
    cliente_nome = models.CharField(max_length=150, verbose_name='Nome')
    cliente_email = models.EmailField(blank=False, null=False, verbose_name='Email')
    cliente_phone = models.CharField(max_length=20, blank=False, null=False, verbose_name="Telefone")
    cliente_cpf = models.CharField('CPF/CNPJ', max_length=14, validators=[validate_cpf, MinLengthValidator(11)],
                                   null=False,
                                   blank=False)
    cliente_endereco = models.CharField(max_length=100, blank=False, null=False, verbose_name="Endereço")
    cliente_data = models.DateField(auto_now_add=True, blank=False, null=False, verbose_name="Data de cadastro")

    class Meta:
        verbose_name_plural = "01-Cadastro de Cliente"

    def __str__(self):
        return self.cliente_nome


# -----------------------Veículos--------------------

class Veiculo(models.Model):
    veiculo_tipo = models.ForeignKey(TipoVeiculo, on_delete=models.CASCADE)
    veiculo_data = models.DateField(auto_now_add=True, blank=False, null=True, verbose_name="Data de cadastro")
    veiculo_placa = models.CharField(max_length=10, verbose_name="Placa do veículo", unique=True)
    veiculo_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    veiculo_operante = models.BooleanField(default=False, blank=False, null=False, verbose_name='Veículo operante')
    veiculo_descricao = models.TextField(blank=True, null=False, verbose_name='Descrição do Veículo')

    class Meta:
        verbose_name_plural = "05-Criação de Veículo"

    def __str__(self):
        return f'{self.veiculo_placa} - {self.veiculo_cliente.cliente_nome}'


# -----------------------Ordem de serviço--------------------


class OrdemServico(models.Model):
    ordem_codigo = models.IntegerField(verbose_name='Código', unique=True, editable=False)
    ordem_placa = models.ForeignKey(
        Veiculo,
        to_field='veiculo_placa',
        verbose_name="Placa e Cliente do veículo",
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
    ordem_grupo_pecas = models.ManyToManyField(
        GrupoPecas,
        verbose_name="Conjunto de Sistema",
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
        verbose_name="Peças trocadas"
    )
    ordem_valor = models.IntegerField(
        default=0,
        verbose_name='Outros Gastos'
    )
    ordem_outros = models.TextField(
        max_length=800,
        blank=True,
        null=False,
        verbose_name='Descrição dos gastos'
    )

    class Meta:
        verbose_name_plural = "06-Ordens de Serviço"

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
