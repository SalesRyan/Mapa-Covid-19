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
from ast import literal_eval
import json
from scripts.agrupamentos.agrupamentos import agrupamento
from scripts.agrupamentos.povoar_atualizar_financeiro import povoar as povoar_financeiro


filterwarnings("ignore")
sheets = authentic()

arq = open('scripts/arquivos/doc.kml', 'rb').read() 
kml = parser.fromstring(arq)


print('povoando casosCidade coordenadas')
[CasosCidade.objects.create(
    nome=unidecode(str(placemark.name)),
    coordenadas=str(placemark.Polygon.outerBoundaryIs.LinearRing.coordinates).strip(),
    ).save() for placemark in kml.Document.Folder.Placemark]


print('povoando casosCidade')
def classAgrupamento(nome):
    objs = DadosFinanceiros.objects.all()
    dicio = {
        'MUNICIPIO':[],
        'VALOR_BF':[],
        'QTD_BF':[],
        'VALOR_AE':[],
        'QTD_AE':[],
        'VALOR_BPC':[],
        'QTD_BPC':[],
        'CONF':[],
        'OBT':[],
        'INC':[],
        'POP':[]
    }
    for obj in objs:
        dicio['MUNICIPIO'].append(obj.cidade.nome)
        dicio['VALOR_BF'].append(obj.valor_bolsa_familia)
        dicio['QTD_BF'].append(obj.quantidade_bolsa_familia)
        dicio['VALOR_AE'].append(obj.valor_auxilio_emergencial)
        dicio['QTD_AE'].append(obj.quantidade_auxilio_emergencial)
        dicio['VALOR_BPC'].append(obj.valor_BPC)
        dicio['QTD_BPC'].append(obj.quantidade_BPC)
        dicio['CONF'].append(obj.cidade.confirmados)
        dicio['OBT'].append(obj.cidade.obitos)
        dicio['INC'].append(obj.cidade.incidencia)
        dicio['POP'].append(obj.cidade.populacao)
    df = pd.DataFrame(dicio)
    df_normalizado = df.apply(lambda x: pd.Series([x[0], x[1]/x[10], x[2]/x[10], x[3]/x[10], x[4]/x[10], x[5]/x[10], x[6]/x[10], x[7]/x[10], x[8]/x[10], x[9]]), axis=1 ,raw=True)
    grupos = agrupamento(df_real=df, df_nor=df_normalizado) 
    grupos = [[cidade.replace("'","") for cidade in grupo] for grupo in grupos]
    for index,grupo in enumerate(grupos):
        if unidecode(nome) in grupo:
            return index
    return -1

df = generateCityDataTable(sheets)
dataset = [CasosCidade.objects.update_or_create(
    nome=d[0],
    defaults = {
        'confirmados':d[1], 
        'obitos':d[2],
        'incidencia':str(d[3]).replace(',', '.'),
        'populacao':d[4],
        'cep':d[5],
        'classe':classAgrupamento(d[0]),
    }) for d in df.values]


print("Povoando a data de atualização")
dataset = [DataAtualizacao.objects.create(
    data=d[0]
    ).save() for d in generateDataUpdateTable(sheets).values]
    
print('povoando leitos')
df_c = generateInternedDataTable(sheets)
dataset = [Leitos.objects.create(
    data=datetime.strptime(str(d[0]),'%d/%m/%Y'),
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

    
# print('povoando DadosEstado')
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



pred_confirmados = pred(df,'Confirmados')
pred_obitos = pred(df,'Óbitos')


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

print("Povoando historico diario")
historico_diario_dict = generateHistoryTable(sheets)
[HistoricoDiario.objects.create(
    regiao=CasosRegioes.objects.get(nome=target_list),
    dados=historico_diario_dict[target_list]) for target_list in historico_diario_dict]

print("Povoando historico de cidade diario")
historico_diario_dict = generateHistoryCityTable(sheets)
[HistoricoCidadesDiario.objects.create(
    cidade=CasosCidade.objects.get(nome=unidecode(target_list).upper()),
    dados=historico_diario_dict[target_list]) for target_list in historico_diario_dict]

print("Povoando Recuperados")
dataset = [Recuperados.objects.create(
    quantidade=d[0],
).save() for d in generateRecoveredTable(sheets).values]

print("Povoando Predição de Regiões")
historicos = HistoricoDiario.objects.all()
for regiao in historicos:
    dados = literal_eval(regiao.dados)
    data_historico_diario = pd.DataFrame({
        'date':list(map(lambda x: x[0], dados)),
        'confirmados':list(map(lambda x: x[1], dados)),
        'obitos':list(map(lambda x: x[2], dados))
    })
    pred_confirmados = pred(data_historico_diario, 'confirmados')
    pred_obitos = pred(data_historico_diario, 'obitos')
    last_date = datetime.strptime(str(dados[-1][0]),"%d/%m/%Y")
    cont = 1
    data = []
    for conf, obt in zip(pred_confirmados, pred_obitos):
        data.append([datetime.strftime(last_date+timedelta(days=cont), '%d/%m/%Y'), int(conf[0]), int(obt[0])])
        cont+=1
    HistoricoDiarioPred.objects.create(
        regiao = regiao.regiao,
        dados = str(data)
    ).save()

print("Povoando Predição de Cidades")
historicos = HistoricoCidadesDiario.objects.all()
for cidades in historicos:
    dados = literal_eval(cidades.dados)
    data_historico_diario = pd.DataFrame({
        'date':list(map(lambda x: x[0], dados)),
        'confirmados':list(map(lambda x: x[1], dados)),
        'obitos':list(map(lambda x: x[2], dados))
    })
    pred_confirmados = predCity(data_historico_diario, 'confirmados')
    pred_obitos = predCity(data_historico_diario, 'obitos')
    last_date = datetime.strptime(str(dados[-1][0]),"%d/%m/%Y")
    cont = 1
    data = []
    for conf, obt in zip(pred_confirmados, pred_obitos):
        data.append([datetime.strftime(last_date+timedelta(days=cont), '%d/%m/%Y'), int(conf[0]), int(obt[0])])
        cont+=1
    HistoricoCidadesDiarioPred.objects.create(
        cidade = cidades.cidade,
        dados = str(data)   
    ).save()

print('Povoando o poligono do PI')
arq = open('scripts/arquivos/PI.json', 'r')
js = json.loads(arq.read())
PoligonoPI.objects.create(poligono = str(js['coords'])).save()

print("Povoando os dados fincanceiro")
povoar_financeiro()

