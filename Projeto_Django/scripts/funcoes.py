from datetime import datetime
from dashboard.models import *

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from warnings import filterwarnings
filterwarnings("ignore")

def CheckValue(df,column): #Função para salvar a coluna caso o valor esteja vazio
    indexs = list(df[df[column]==''].index)
    if indexs:
        for index in indexs:
            df[column][index] = df[column][index-1]
    return df

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
    
    df = getData(sheets,index=28)
    
    df = CheckValue(df,'Capacidade Leitos Clínicos')
    df = CheckValue(df,'Capacidade UTI')
    df = CheckValue(df,'Capacidade LE')
    df = CheckValue(df,'Capacidade Leitos Respiradores')

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
    df = getData(sheets,index=6)
    df = df[df['Município']!='PIAUÍ']
    df = df[df['Município']!='']
    d = {
        'Município':df['Município'].to_list(),
        'Confirmados':df['Confirmados'].to_list(),
        'Óbitos':df['Óbitos'].to_list(),
        'Incidência':df['Incidência'].to_list(),
        'CEP':df['CEP'].to_list()
    }

    return pd.DataFrame(data=d).replace({'': 0})

def generateStateDataTable(sheets):
    df = getData(sheets,index=8)

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
    df = df[df['Faixa Etária']!='TOTAL']
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



    # Predições

def getcolumn(df,column,verbose=0): #Retorna o X e  y respectivamente
    X, y = df[column].index.ravel().reshape(-1,1), df[column].values.ravel().reshape(-1,1)
    if verbose:
        print("column: {} CSV X shape: {} Max: {} Min: {}".format(column,X.shape,X.max(),X.min()))
        print("column: {} CSV y shape: {} Max: {} Min: {}".format(column,y.shape,y.max(),y.min()))
    return X,y

def Pred(X_train, X_test, y_train, y_test=None):
    
    degree = 4

    modelo_polinomial = make_pipeline(PolynomialFeatures(degree), Ridge())
    modelo_polinomial.fit(X_train, y_train)

    pred_values = modelo_polinomial.predict(X_test)
    pred = np.int_(pred_values)

    return pred
    

def PredFull(df,mode=30,name='Confirmados'):
    X_train, y_train = getcolumn(df,name,verbose=0)
    x_max = X_train.max()+1
    X_test = np.asarray(range(x_max,x_max+mode)).reshape(-1,1)
    pred = Pred(X_train, X_test, y_train)

    return pred



def pred_de(X_train,y_train,X_test):
 
    degree = 2

    modelo_polinomial = make_pipeline(PolynomialFeatures(degree), Ridge())
    modelo_polinomial.fit(X_train, y_train)

    pred_values = modelo_polinomial.predict(X_test)
    pred = np.int_(pred_values)
    return pred
    

def pred_clinical(csv,mode=7):

    CapacidadeLC = np.int_(csv['Capacidade Leitos Clínicos'].values.reshape(-1,1))
    InternadosLC = np.int_(csv['Internados Leitos Clínicos'].values.reshape(-1,1))

    CapacidadeUTI = np.int_((csv['Capacidade UTI'].values.reshape(-1,1)))
    InternadosUTI = np.int_((csv['Internados UTI'].values.reshape(-1,1)))

    CapacidadeLE = np.int_((csv['Capacidade LE'].values.reshape(-1,1)))
    InternadosLE = np.int_((csv['Internados Estabilização'].values.reshape(-1,1)))

    CapacidadeLR = np.int_(csv['Capacidade Leitos Respiradores'].values.reshape(-1,1))
    InternadosLR = np.int_(csv['Internados Leitos Respiradores'].values.reshape(-1,1))

    index = np.asarray(csv['Dias'].index).reshape(-1,1)
    LC = np.int_((InternadosLC/CapacidadeLC)*100)
    UTI = np.int_((InternadosUTI/CapacidadeUTI)*100)
    LE = np.int_((InternadosLE/CapacidadeLE)*100)
    LR = np.int_((InternadosLR/CapacidadeLR)*100)

    x_max = index.max()+1
    X_test = np.asarray(range(x_max,x_max+mode)).reshape(-1,1)

    p_LC = pred_de(index,LC,X_test)
    p_UTI = pred_de(index,UTI,X_test)
    p_LE = pred_de(index,LE,X_test)
    p_LR = pred_de(index,LR,X_test)

    return {'index':X_test,'LC':p_LC,'UTI':p_UTI,'LE':p_LE,'LR':p_LR}