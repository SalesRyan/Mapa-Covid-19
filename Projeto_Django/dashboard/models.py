from django.db import models
from core.models import AuditModel

# Create your models here.
class DadosEstado(AuditModel):
    data = models.DateTimeField("Data de modificação", auto_now=False, auto_now_add=False,null=True, blank=True)
    confirmados = models.IntegerField("Confirmados", null=True, blank=True)
    obitos = models.IntegerField("Obitos", null=True, blank=True)

class CasosCidade(AuditModel):
    nome = models.TextField("Nome da cidade", max_length=45,null=True, blank=True)
    confirmados = models.IntegerField("Confirmados",null=True, blank=True)
    obitos = models.IntegerField("Obitos",null=True, blank=True)
    incidencia = models.FloatField("Incidencia", null=True, blank=True)
    cep = models.TextField("CEP", max_length=9,null=True, blank=True)

class Leitos(AuditModel):
    data = models.DateTimeField("Data de modificação", auto_now=False, auto_now_add=False)
    capacidade_clinicos = models.IntegerField("Capacidade Clinicos", null=True, blank=True)
    ocupados_clinicos = models.IntegerField("Ocupados Clinicos", null=True, blank=True)
    capacidade_uti = models.IntegerField("Capacidade UTI", null=True, blank=True)
    ocupados_uti = models.IntegerField("Ocupados UTI", null=True, blank=True)
    capacidade_estabilizacao = models.IntegerField("Capacidade Estabilizacao", null=True, blank=True)
    ocupados_estabilizacao = models.IntegerField("Ocupados Estabilizacao", null=True, blank=True)
    capacidade_respiradores = models.IntegerField("Capacidade Respiradores", null=True, blank=True)
    ocupados_respiradores = models.IntegerField("Ocupados Respiradores", null=True, blank=True)
    altas = models.IntegerField("Altas", null=True, blank=True)


class CasosSexo(AuditModel):
    obitos_masculinos = models.IntegerField("Obitos Masculinos", null=True, blank=True)
    obitos_femininos = models.IntegerField("Obitos Femininos", null=True, blank=True)
    casos_masculinos = models.IntegerField("Casos Masculinos", null=True, blank=True)
    casos_femininos = models.IntegerField("Casos Femininos", null=True, blank=True)

class CasosFaixaEtaria(AuditModel):
    faixa_etaria = models.TextField("Nome da Faixa Etaria", max_length=45,null=True, blank=True)
    confirmados = models.IntegerField("Obitos Masculinos", null=True, blank=True)
    obitos = models.IntegerField("Obitos Femininos", null=True, blank=True)


class Comorbidades(AuditModel):
    nome = models.TextField("Nome da Comorbidade", max_length=45,null=True, blank=True)
    quantidade = models.IntegerField("Obitos Masculinos", null=True, blank=True)









