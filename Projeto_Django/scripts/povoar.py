#!/usr/bin/env python
# coding: utf-8

#models

from datetime import datetime
from dashboard.models import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from warnings import filterwarnings
from scripts.Funcoes import *
filterwarnings("ignore")

sheets = authentic()

print("Povoando a data de atualização")
dataset = dataset = [DataAtualizacao.objects.create(
    data=d[0]
    ).save() for d in generateDataUpdateTable(sheets).values]
    
print('povoando leitos')
dataset = [Leitos.objects.create(
    data=datetime.strptime(d[0],'%d/%m/%Y'),
    capacidade_clinicos=d[1],
    ocupados_clinicos=d[2],
    capacidade_uti=d[3],
    ocupados_uti=d[4],
    capacidade_estabilizacao=d[5],
    ocupados_estabilizacao=d[6],
    capacidade_respiradores=d[7],
    ocupados_respiradores=d[8],
    altas=d[9],
    ).save() for d in generateInternedDataTable(sheets).values]

print('povoando casosCidade')
print(len(generateCityDataTable(sheets).values))
dataset = [CasosCidade.objects.create(
    nome=d[0],
    confirmados=d[1], 
    obitos=d[2],
    incidencia=str(d[3]).replace(',', '.'),
    cep=d[4],
    ).save() for d in generateCityDataTable(sheets).values]
    
print('povoando DadosEstado')
dataset = [DadosEstado.objects.create(
    data=datetime(2020, int(d[0].split('/')[1]), int(d[0].split('/')[0])),
    confirmados=d[1],
    obitos=d[2],
    ).save() for d in generateStateDataTable(sheets).values] 

print('povoando Comorbidades')
dataset = [Comorbidades.objects.create(
        nome=d[0], 
        quantidade=d[1], 
    ).save() for d in generateComorbidityTable(sheets).values]

print('povoando Faixa Etaria')
dataset = [CasosFaixaEtaria.objects.create(
        faixa_etaria=d[0], 
        confirmados=d[1], 
        obitos=d[2],
    ).save() for d in generateAgeRangeTable(sheets).values]
    
print("Povoando casos sexo")
dataset = [CasosSexo.objects.create(
        obitos_masculinos=d[0],
        obitos_femininos=d[1],
        casos_masculinos=d[2],
        casos_femininos=d[3],
    ).save() for d in generateGenderTable(sheets).values]