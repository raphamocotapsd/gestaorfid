from django.contrib import admin
from .models import *


# -----------Cadastros primarios--------
@admin.register(PecasVeiculo)
class PecasAdmin(admin.ModelAdmin):
    list_display = ('pecas_veiculo',)


@admin.register(TipoVeiculo)
class TipoVeiculoAdmin(admin.ModelAdmin):
    list_display = ('tipoVeiculo',)


# ----------Cadastros grupo---------

@admin.register(GrupoPecas)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('grupo_pecas', 'grupo_description')
    filter_horizontal = ('pecas_veiculo',)


# ---------Cadastros Veículo
@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_filter = ('veiculo_tipo', 'veiculo_operante', 'veiculo_cliente','veiculo_data')
    list_display = ('veiculo_placa', 'veiculo_tipo', 'veiculo_operante', 'veiculo_cliente','veiculo_data')


# ---------Cadastros Cliente--------------
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente_nome', 'cliente_email', 'cliente_phone', 'cliente_data')
    list_filter = ('cliente_nome', 'cliente_data')


# ---------Ordem de Serviço--------------
@admin.register(OrdemServico)
class OrdemAdmin(admin.ModelAdmin):
    list_display = ('ordem_codigo', 'ordem_placa', 'ordem_data', 'ordem_classificacao', 'ordem_valor')
    list_filter = ('ordem_classificacao', 'ordem_data')
    filter_horizontal = ('ordem_grupo_pecas','pecas_grupo')
