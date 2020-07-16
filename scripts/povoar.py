#!/usr/bin/env python
# coding: utf-8

#models
from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from unidecode import unidecode
from os import path
from lxml import etree

from datetime import datetime, timedelta
from dashboard.models import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from warnings import filterwarnings
from scripts.funcoes import *


filterwarnings("ignore")
sheets = authentic()

arq = open('scripts/arquivos/doc.kml', 'rb').read() 
kml = parser.fromstring(arq)

dataset = [CasosCidade.objects.create(
    nome=unidecode(str(placemark.name)),
    coordenadas=str(placemark.Polygon.outerBoundaryIs.LinearRing.coordinates).strip(),
    ).save() for placemark in kml.Document.Folder.Placemark]

print('povoando casosCidade')
df = generateCityDataTable(sheets)
dataset = [CasosCidade.objects.update_or_create(
    nome=d[0],
    defaults = {
        'confirmados':d[1], 
        'obitos':d[2],
        'incidencia':str(d[3]).replace(',', '.'),
        'cep':d[4],
    }) for d in df.values]

print("Povoando a data de atualização")
dataset = [DataAtualizacao.objects.create(
    data=d[0]
    ).save() for d in generateDataUpdateTable(sheets).values]
    
print('povoando leitos')
df_c = generateInternedDataTable(sheets)
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
    ).save() for d in df_c.values]

    
print('povoando DadosEstado')
df = generateStateDataTable(sheets)
dataset = [DadosEstado.objects.create(
    data=datetime(2020, int(d[0].split('/')[1]), int(d[0].split('/')[0])),
    confirmados=d[1],
    obitos=d[2],
    ).save() for d in df.values] 

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

pred_confirmados = PredFull(df,mode=14,name='Confirmados')
pred_obitos = PredFull(df,mode=14,name='Óbitos')
last_date = list(df['Dias'])[-1]
last_date = datetime.strptime(last_date+'/2020','%d/%m/%Y')
count = 1
for conf, obt in zip(pred_confirmados, pred_obitos):
    DadosEstadoPredicao.objects.create(
        data=last_date+timedelta(days=count),
        confirmados=conf,
        obitos=obt
    ).save()
    count += 1

pred_leitos = pred_clinical(df_c,mode=3)
# pred_obitos = PredFull(df,mode=14,name='Óbitos')
last_date = list(df_c['Dias'])[-1]
last_date = datetime.strptime(last_date,'%d/%m/%Y')
count = 1
for LC, UTI, LE, LR in zip(pred_leitos['LC'], pred_leitos['UTI'], pred_leitos['LE'], pred_leitos['LR']):
    LeitosPredicao.objects.create(
        data=last_date+timedelta(days=count),
        taxa_ocupados_clinicos=LC,
        taxa_ocupados_uti=UTI,
        taxa_ocupados_estabilizacao=LE,
        taxa_ocupados_respiradores=LR
    ).save()
    count += 1
