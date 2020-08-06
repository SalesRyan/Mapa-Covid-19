from django.db import models
from core.models import AuditModel

# Create your models here.
class DataAtualizacao(models.Model):
    data = models.CharField("Data de atualização da planilha", max_length=45)

class DadosEstado(AuditModel):
    data = models.DateTimeField("Data de modificação", auto_now=False, auto_now_add=False,null=True, blank=True,unique=True )
    confirmados = models.IntegerField("Confirmados", null=True, blank=True)
    obitos = models.IntegerField("Obitos", null=True, blank=True)

class DadosEstadoPredicao(AuditModel):
    data = models.DateTimeField("Data de modificação", auto_now=False, auto_now_add=False,null=True, blank=True)
    confirmados = models.IntegerField("Confirmados", null=True, blank=True)
    obitos = models.IntegerField("Obitos", null=True, blank=True)

class CasosCidade(AuditModel):
    nome = models.CharField("Nome da cidade", max_length=45,null=True, blank=True, unique=True)
    confirmados = models.IntegerField("Confirmados",null=True, blank=True, default=0)
    obitos = models.IntegerField("Obitos",null=True, blank=True, default=0)
    incidencia = models.FloatField("Incidencia", null=True, blank=True, default=0)
    cep = models.CharField("CEP", max_length=9,null=True, blank=True)
    coordenadas = models.TextField("Coordenadas")
    populacao = models.IntegerField("População", null=True, blank=True, default=0)
    regiao = models.ForeignKey("dashboard.CasosRegioes", verbose_name="Região", on_delete=models.DO_NOTHING, null=True)
    
    def __str__(self):
        return self.nome

class CasosRegioes(AuditModel):
    nome = models.CharField("Nome da cidade", max_length=45,null=True, blank=True, unique=True)
    confirmados = models.IntegerField("Confirmados",null=True, blank=True, default=0)
    obitos = models.IntegerField("Obitos",null=True, blank=True, default=0)
    coordenadas = models.TextField("Coordenadas")
    incidencia = models.FloatField("Incidencia", null=True, blank=True, default=0)

    
    def __str__(self):
        return self.nome
    

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

class LeitosPredicao(AuditModel):
    data = models.DateTimeField("Dia", null=True, blank=True)
    taxa_ocupados_clinicos = models.FloatField("Ocupados Clinicos", null=True, blank=True)
    taxa_ocupados_uti = models.FloatField("Ocupados UTI", null=True, blank=True)
    taxa_ocupados_estabilizacao = models.FloatField("Ocupados Estabilizacao", null=True, blank=True)
    taxa_ocupados_respiradores = models.FloatField("Ocupados Respiradores", null=True, blank=True)

class CasosSexo(AuditModel):
    obitos_masculinos = models.IntegerField("Obitos Masculinos", null=True, blank=True)
    obitos_femininos = models.IntegerField("Obitos Femininos", null=True, blank=True)
    casos_masculinos = models.IntegerField("Casos Masculinos", null=True, blank=True)
    casos_femininos = models.IntegerField("Casos Femininos", null=True, blank=True)

class CasosFaixaEtaria(AuditModel):
    faixa_etaria = models.CharField("Nome da Faixa Etaria", max_length=45,null=True, blank=True,unique=True)
    confirmados = models.IntegerField("Casos Confirmados", null=True, blank=True)
    obitos = models.IntegerField("Óbitos", null=True, blank=True)

    def __str__(self):
        return self.faixa_etaria

class Comorbidades(AuditModel):
    nome = models.CharField("Nome da Comorbidade", max_length=45,null=True, blank=True, unique=True)
    quantidade = models.IntegerField("Quantidade", null=True, blank=True)

    def __str__(self):
        return self.nome

class HistoricoDiario(AuditModel): #por regiao
    regiao = models.ForeignKey("dashboard.CasosRegioes", verbose_name="Regiao", on_delete=models.DO_NOTHING, null=True)
    dados = models.CharField("Data de Postagem",null=True, blank=True,max_length=1000000)
    # confirmados = models.IntegerField("Confirmados", null=True, blank=True, default=0)
    # obitos = models.IntegerField("Óbitos", null=True, blank=True, default=0)

 