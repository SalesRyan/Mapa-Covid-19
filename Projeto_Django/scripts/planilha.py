#!/usr/bin/env python
# coding: utf-8

#models
from datetime import datetime
from dashboard.models import *

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from warnings import filterwarnings
filterwarnings("ignore")

def authentic():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    try:

        creds = ServiceAccountCredentials.from_json_keyfile_name('scripts/creds.json', scope)


    except Exception as e:

        print(e)

    client = gspread.authorize(creds)
    return client.open_by_key('1b-GkDhhxJIwWcA6tk3z4eX58f-f1w2TA2f2XrI4XB1w')


def getData(sheets,index=0):

    #Convertendo os dados da planilha para um DataFrame Para pegar todas basta iterar sobre sheets.worksheets()

    data = sheets.worksheets()[index].get_all_values()
    headers = data.pop(0)
    return pd.DataFrame(data, columns = headers)

sheets = authentic()

def generateInternedDataTable(sheets):
    
    df = getData(sheets,index=23)
    
    d = {
        'Dias':df['Dias'].to_list(),
        'Capacidade Leitos Clínicos':df['Capacidade Leitos Clínicos'].to_list(),
        'Internados Leitos Clínicos':df['Internados Leitos Clínicos'].to_list(),
        'Capacidade UTI':df['Capacidade UTI'].to_list(),
        'Internados UTI':df['Internados UTI'].to_list(),
        'Capacidade LE':df['Capacidade LE'].to_list(),
        'Internados Estabilização':df['Internados Estabilização'].to_list(),
        'Capacidade Leitos Respiradores':df['Capacidade Leitos Respiradores'].to_list(),
        'Internados Leitos Respiradores':df['Internados Leitos Respiradores'].to_list(),
        'Altas':df['Altas'].to_list()
    }
    return pd.DataFrame(data=d).replace({'': 0})

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

def generateCityDataTable(sheets):
    df = getData(sheets,index=6)
    d = {
        'Município':df['Município'].to_list(),
        'Confirmados':df['Confirmados'].to_list(),
        'Óbitos':df['Óbitos'].to_list(),
        'Incidência':df['Incidência'].to_list(),
        'CEP':df['CEP'].to_list()
    }
    return pd.DataFrame(data=d).replace({'': 0})

dataset = [CasosCidade.objects.create(
    nome=d[0],
    confirmados=d[1], 
    obitos=d[2],
    incidencia=d[3].replace(',', '.'),
    cep=d[4],
    ).save() for d in generateCityDataTable(sheets).values]  

def generateStateDataTable(sheets):
    df = getData(sheets,index=5)
    d = {
        'Dias':df['Dias'].to_list(),
        'Confirmados':df['Confirmados'].to_list(),
        'Óbitos':df['Óbitos'].to_list(),
    }
    return pd.DataFrame(data=d).replace({'': 0})

dataset = [DadosEstado.objects.create(
    data=datetime(2020, int(d[0].split('/')[1]), int(d[0].split('/')[0])),
    confirmados=d[1],
    obitos=d[2],
    ).save() for d in generateStateDataTable(sheets).values] 
   
def generateComorbidityTable(sheets):
    df = getData(sheets,index=4)
    d = {
        'Morbidades':df['Morbidades'].to_list(),
        'Qtde':df['Qtde'].to_list(),
    }
    return pd.DataFrame(data=d).replace({'': 0})

dataset = [Comorbidades.objects.create(
        nome=d[0], 
        quantidade=d[1], 
    ).save() for d in generateComorbidityTable(sheets).values]

def generateAgeRangeTable(sheets):
    df = getData(sheets,index=3)
    d = {
        'Faixa Etária':df['Faixa Etária'].to_list(),
        'Confirmados':df['Confirmados'].to_list(),
        'Óbitos':df['Óbitos'].to_list()
    }
    return pd.DataFrame(data=d).replace({'': 0})

dataset = [CasosFaixaEtaria.objects.create(
        faixa_etaria=d[0], 
        confirmados=d[1], 
        obitos=d[2],
    ).save() for d in generateAgeRangeTable(sheets).values]

def generateGenderTable(sheets):
    df1 = getData(sheets,index=1)
    df2 = getData(sheets,index=2)
    d = {
        'Obitos Masculino':list(df2[df2.Sexo=="Masculino"].Quantidade),
        'Obitos Feminino':list(df2[df2.Sexo=="Feminino"].Quantidade),
        'Confirmados Masculino':list(df1[df1.Sexo=="Masculino"].Quantidade),
        'Confirmados Feminino':list(df1[df1.Sexo=="Feminino"].Quantidade),
    }
    return pd.DataFrame(data=d).replace({'': 0})

dataset = [CasosSexo.objects.create(
        obitos_masculinos=d[0],
        obitos_femininos=d[1],
        casos_masculinos=d[2],
        casos_femininos=d[3],
    ).save() for d in generateGenderTable(sheets).values]