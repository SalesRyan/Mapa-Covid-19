from scripts.Funcoes import *
import pandas as pd
from scripts.email import mail

def authenticCheck():
    try:
        sheets = authentic()
    except Exception as e:
        mail('Exception on Verificar.authenticCheck', str(e))
        return pd.DataFrame({'':[]})
    else:
        if not sheets:
            mail('Error on Verificar.authenticCheck', 'Empty sheet')
            return pd.DataFrame({'':[]})
    return sheets

def getDataCheck(sheets):
    try:
        var = getData(sheets,index=0)
    except Exception as e:
        mail('Exception on Verificar.getDataCheck', str(e))
        return pd.DataFrame({'':[]})
    else:
        if var.empty:
            mail('Error on Verificar.authenticCheck', 'Empty sheet')
            return pd.DataFrame({'':[]})
    return var

def generateInternedDataTableCheck(sheets):
    try:
        var = generateInternedDataTable(sheets)
    except Exception as e:
        mail('Exception on Verificar.generateInternedDataTableCheck', str(e))
        return pd.DataFrame({'':[]}) 
    else:
        if ['Dias',
            'Capacidade Leitos Clínicos',
            'Internados Leitos Clínicos',
            'Capacidade UTI',
            'Internados UTI',
            'Capacidade LE',
            'Internados Estabilização',
            'Capacidade Leitos Respiradores',
            'Internados Leitos Respiradores',
            'Altas'] != list(var):
            mail('Error on Verificar.generateInternedDataTableCheck', 'Cabeçalho incorreto')
            return pd.DataFrame({'':[]})
    return var


def generateCityDataTableCheck(sheets):
    try:
        var = generateCityDataTable(sheets)
    except Exception as e:
        mail('Exception on Verificar.generateCityDataTableCheck', str(e))
        return pd.DataFrame({'':[]})
    else:
        if ['Município', 
            'Confirmados', 
            'Óbitos', 
            'Incidência',
            'CEP'] != list(var):
            mail('Error on Verificar.generateCityDataTable', 'Cabeçalho incorreto')
            return pd.DataFrame({'':[]})
    return var

def generateStateDataTableCheck(sheets):

    try:
        var = generateStateDataTable(sheets)
    except Exception as e:
        mail('Exception on Verificar.generateStateDataTable', str(e))
        return pd.DataFrame({'':[]})
    else:
        if ['Dias',
            'Confirmados',
            'Óbitos'] != list(var):
            mail('Error on Verificar.generateStateDataTable', 'Cabeçalho Incorreto')
            return pd.DataFrame({'':[]})
    return var

def generateComorbidityTableCheck(sheets):
    try:
        var = generateComorbidityTable(sheets)
    except Exception as e:
        mail('Exception on Verificar.generateComorbidityTableCheck', str(e))
        return pd.DataFrame({'':[]})
    else:
        if ['Morbidades',
            'Qtde'] != list(var):
            mail('Error on Verificar.generateComorbidityTable', 'Cabeçalho Incorreto')
            return pd.DataFrame({'':[]})
    return var

def generateAgeRangeTableCheck(sheets):
    try:
        var = generateAgeRangeTable(sheets)
    except Exception as e:
        mail('Exception on Verificar.generateAgeRangeTableCheck', str(e))
        return pd.DataFrame({'':[]})
    else:
        if ['Faixa Etária', 
            'Confirmados', 
            'Óbitos'] != list(var):
            mail('Error on Verificar.generateAgeRangeTableCheck', 'Cabeçalho Incorreto')
            return pd.DataFrame({'':[]})
    return var

def generateGenderTableCheck(sheets):
    try:
        var = generateGenderTable(sheets)
    except Exception as e:
        mail('Exception on Verificar.generateGenderTableCheck', str(e))
        return pd.DataFrame({'':[]})
    else:
        if ['Obitos Masculino',
            'Obitos Feminino',
            'Confirmados Masculino',
            'Confirmados Feminino'] != list(var):
            mail('Error on Verificar.generateGenderTableCheck', 'Cabeçalho Incorreto')
            return pd.DataFrame({'':[]})
    return var

def check():
    sheets = authenticCheck()
    return {
        'Leitos':generateInternedDataTableCheck(sheets),
        'CasosCidade':generateCityDataTableCheck(sheets),
        'DadosEstado':generateStateDataTableCheck(sheets),
        'Comorbidades':generateComorbidityTableCheck(sheets),
        'CasosFaixaEtaria':generateAgeRangeTableCheck(sheets),
        'CasosSexo':generateGenderTableCheck(sheets)
    }