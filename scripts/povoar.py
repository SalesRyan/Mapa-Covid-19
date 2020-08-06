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
from django.db.models import Sum



filterwarnings("ignore")
sheets = authentic()

# arq = open('scripts/arquivos/doc.kml', 'rb').read() 
# kml = parser.fromstring(arq)


# print('povoando casosCidade coordenadas')
# [CasosCidade.objects.create(
#     nome=unidecode(str(placemark.name)),
#     coordenadas=str(placemark.Polygon.outerBoundaryIs.LinearRing.coordinates).strip(),
#     ).save() for placemark in kml.Document.Folder.Placemark]


# print('povoando casosCidade')
# df = generateCityDataTable(sheets)
# dataset = [CasosCidade.objects.update_or_create(
#     nome=d[0],
#     defaults = {
#         'confirmados':d[1], 
#         'obitos':d[2],
#         'incidencia':str(d[3]).replace(',', '.'),
#         'populacao':d[4],
#         'cep':d[5],
#     }) for d in df.values]

# print("Povoando a data de atualização")
# dataset = [DataAtualizacao.objects.create(
#     data=d[0]
#     ).save() for d in generateDataUpdateTable(sheets).values]
    
# print('povoando leitos')
# df_c = generateInternedDataTable(sheets)
# dataset = [Leitos.objects.create(
#     data=datetime.strptime(str(d[0]),'%d/%m/%Y'),
#     capacidade_clinicos=d[1],
#     ocupados_clinicos=d[2],
#     capacidade_uti=d[3],
#     ocupados_uti=d[4],
#     capacidade_estabilizacao=d[5],
#     ocupados_estabilizacao=d[6],
#     capacidade_respiradores=d[7],
#     ocupados_respiradores=d[8],
#     altas=d[9],
#     ).save() for d in df_c.values]

    
# print('povoando DadosEstado')
# df = generateStateDataTable(sheets)
# dataset = [DadosEstado.objects.create(
#     data=datetime(2020, int(d[0].split('/')[1]), int(d[0].split('/')[0])),
#     confirmados=d[1],
#     obitos=d[2],
#     ).save() for d in df.values] 

# print('povoando Comorbidades')
# dataset = [Comorbidades.objects.create(
#         nome=d[0], 
#         quantidade=d[1], 
#     ).save() for d in generateComorbidityTable(sheets).values]

# print('povoando Faixa Etaria')
# dataset = [CasosFaixaEtaria.objects.create(
#         faixa_etaria=d[0], 
#         confirmados=d[1], 
#         obitos=d[2],
#     ).save() for d in generateAgeRangeTable(sheets).values]
    
# print("Povoando casos sexo")
# dataset = [CasosSexo.objects.create(
#         obitos_masculinos=d[0],
#         obitos_femininos=d[1],
#         casos_masculinos=d[2],
#         casos_femininos=d[3],
#     ).save() for d in generateGenderTable(sheets).values]

print("Povoando historico diario")
# print(dir(generateHistoryTable(sheets)))
historico_diario_dict = generateHistoryTable(sheets)
for target_list in historico_diario_dict:
    print(target_list)
    HistoricoDiario.objects.create(regiao=CasosRegioes.objects.get(nome=target_list),dados=historico_diario_dict[target_list])


# for d in generateHistoryTable(sheets).values:
#     ob = HistoricoDiario.objects.update_or_create(
#         data=datetime(int(d[0].split('/')[2]), int(d[0].split('/')[1]), int(d[0].split('/')[0])),
#         regiao=CasosCidade.objects.get(nome=unidecode(d[1]).upper()).regiao,
#     )

#     # print(ob[0].id)
#     ob[0].confirmados = int(d[2])
#     ob[0].obitos = int(d[3])
#     ob[0].save()

exit(-1)

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
last_date = datetime.strptime(str(last_date),'%d/%m/%Y')
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

arq_regiao = open('scripts/arquivos/doc_regiao.kml', 'rb').read() 
kml_regiao = parser.fromstring(arq_regiao)

print('povoando CasosRegioes coordenadas')
dataset = [CasosRegioes.objects.create(
    nome=unidecode(str(placemark.name)).upper(),
    coordenadas=str(placemark.Polygon.outerBoundaryIs.LinearRing.coordinates).replace(" ","").replace("\n", " ").strip(),
    ).save() for placemark in kml_regiao.Document.Placemark]

regioes = json.loads(open('scripts/arquivos/regioes.json', 'r').read())
for key, value in regioes.items():
    for cidade in value:
        # print("aqui\n\n",CasosRegioes.objects.get(nome=unidecode(key).upper()))
        CasosCidade.objects.update_or_create(
            nome=cidade,
            defaults={
                'regiao': CasosRegioes.objects.get(nome=unidecode(key).upper()),
            }
        )

for obj in CasosRegioes.objects.all():
    casos_cidade = CasosCidade.objects.filter(regiao=obj)
    obj.obitos = casos_cidade.aggregate(Sum('obitos'))['obitos__sum']
    obj.confirmados = casos_cidade.aggregate(Sum('confirmados'))['confirmados__sum']
    obj.incidencia = obj.confirmados*10000/(sum([casos.populacao for casos in casos_cidade]))
    obj.save()
