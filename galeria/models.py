from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # Para login (username, password)
    nome = models.CharField(max_length=120)   # Para mostrar na UI
    cnpj = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    data_associacao = models.DateField(auto_now_add=True)
    unidade_geradora = models.CharField(max_length=20)  # Nº da UC do Gerador Solar peranta aa distribuidora
    tipo = models.CharField(max_length=10, choices=[('gerador', 'Gerador'), ('consumidor', 'Consumidor'), ('prosumidor', 'Prosumidor')])
    legenda = models.CharField(max_length=200, blank=True)   # pode ser uma descrição do cliente a ser exibida
    data_atualizacao = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f'{self.nome}-{self.cnpj}'

class Macro(models.Model):
    data_coleta = models.DateField()
    total_geracao_distribuida_mw = models.DecimalField(max_digits=10, decimal_places=2)
    numero_empreendimentos = models.IntegerField()
    potencia_instalada = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=2)
    tipo_geracao = models.CharField(max_length=20, choices=[('solar', 'Solar'), ('eolica', 'Eólica'), ('hidro', 'Hidrelétrica')])
    distribuidora = models.CharField(max_length=100)
    fonte = models.CharField(max_length=50, default='ANEEL')
    
    def __str__(self):
        return f'Dados Macro - {self.estado} - {self.data_coleta}'

class Micro(models.Model):    
    data_leitura = models.DateField()
    energia_gerada_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    energia_consumida_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_creditos = models.DecimalField(max_digits=10, decimal_places=2)
    valor_compensacao = models.DecimalField(max_digits=10, decimal_places=2)
    mes_referencia = models.DateField()  # Armazena primeiro dia do mês de referência
    uc_geradora = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Dados {self.uc_geradora} - {self.mes_referencia}'

    class Meta:
        # Evita duplicidade de registros para mesma UC e mês
        unique_together = ['uc_geradora', 'mes_referencia']

class BaseMicro(models.Model):
    mes_ref = models.DateField()
    dt_vcto = models.DateField()
    id_client = models.IntegerField()
    id_uc = models.IntegerField()
    grandezas = models.CharField(max_length=100)
    leitura_anterior = models.FloatField(null=True, blank=True)
    leitura_atual = models.FloatField(null=True, blank=True)
    const_medidor = models.FloatField(null=True, blank=True)
    consumo_kwh = models.FloatField(null=True, blank=True)
    prc_unit_tributos_tusd = models.FloatField(null=True, blank=True)
    tarifa_unit_tusd = models.FloatField(null=True, blank=True)
    prc_unit_tributos_te = models.FloatField(null=True, blank=True)
    tarifa_unit_te = models.FloatField(null=True, blank=True)
    qtd_enrg_compensada_tusd = models.FloatField(null=True, blank=True)
    prc_unit_tributos_compensada_tusd = models.FloatField(null=True, blank=True)
    tarifa_unit_compensada_tusd = models.FloatField(null=True, blank=True)
    qtd_enrg_compensada_te = models.FloatField(null=True, blank=True)
    prc_unit_tributos_compensada_te = models.FloatField(null=True, blank=True)
    tarifa_unit_compensada_te = models.FloatField(null=True, blank=True)
    cred_prox_fat = models.FloatField(null=True, blank=True)
    total = models.FloatField()
    pis_cofins_total = models.FloatField(null=True, blank=True)
    icms_total = models.FloatField(null=True, blank=True)
    tipo = models.CharField(max_length=50)
    tarifas = models.FloatField(null=True, blank=True)
    solar = models.FloatField(null=True, blank=True)
    impostos = models.FloatField(null=True, blank=True)
    juros = models.FloatField(null=True, blank=True)
    ress = models.FloatField(null=True, blank=True)
    outros = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"UC {self.id_uc} - {self.mes_ref}"
