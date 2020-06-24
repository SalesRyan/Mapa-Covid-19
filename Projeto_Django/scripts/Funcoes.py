from datetime import datetime
from dashboard.models import *

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


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


def generateDataUpdateTable(sheets):
    
    df = getData(sheets,index=9)

    d = {
        'Data de Atualização':df['Data'].to_list(),
    }
    return pd.DataFrame(data=d).replace({'': 0})
    
def generateInternedDataTable(sheets):
    
    df = getData(sheets,index=24)
    
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

def generateCityDataTable(sheets):
    df = getData(sheets,index=7)

    d = {
        'Município':df['Município'].to_list().remove(''),
        'Confirmados':df['Confirmados'].to_list().remove(''),
        'Óbitos':df['Óbitos'].to_list().remove(''),
        'Incidência':df['Incidência'].to_list().remove(''),
        'CEP':df['CEP'].to_list().remove('')
    }
    return pd.DataFrame(data=d)

def generateStateDataTable(sheets):
    df = getData(sheets,index=6)

    d = {
        'Dias':df['Dias'].to_list(),
        'Confirmados':df['Confirmados'].to_list(),
        'Óbitos':df['Óbitos'].to_list(),
    }
    return pd.DataFrame(data=d).replace({'': 0})

def generateComorbidityTable(sheets):
    df = getData(sheets,index=5)
    
    d = {
        'Morbidades':df['Morbidades'].to_list(),
        'Qtde':df['Qtde'].to_list(),
    }
    return pd.DataFrame(data=d).replace({'': 0})

def generateAgeRangeTable(sheets):
    df = getData(sheets,index=4)
    d = {
        'Faixa Etária':df['Faixa Etária'].to_list(),
        'Confirmados':df['Confirmados'].to_list(),
        'Óbitos':df['Óbitos'].to_list()
    }
    return pd.DataFrame(data=d).replace({'': 0})

def generateGenderTable(sheets):
    df1 = getData(sheets,index=2)
    df2 = getData(sheets,index=3)
    d = {
        'Obitos Masculino':list(df2[df2.Sexo=="Masculino"].Quantidade),
        'Obitos Feminino':list(df2[df2.Sexo=="Feminino"].Quantidade),
        'Confirmados Masculino':list(df1[df1.Sexo=="Masculino"].Quantidade),
        'Confirmados Feminino':list(df1[df1.Sexo=="Feminino"].Quantidade),
    }
    return pd.DataFrame(data=d).replace({'': 0})

def getData(sheets,index=0):

    #Convertendo os dados da planilha para um DataFrame Para pegar todas basta iterar sobre sheets.worksheets()

    data = sheets.worksheets()[index].get_all_values()
    headers = data.pop(0)
    return pd.DataFrame(data, columns = headers)