from scripts.Funcoes import *
import pandas as pd


def authenticCheck():
    try:
        sheets = authentic()
    except Exception as e:
        print(e)
        return False
    else:
        if not sheets:
            print("Função de email authenticCheck")
            return False
    return True

def getDataCheck():
    try:
        var = getData(authentic(),index=0)
    except Exception as e:
        print(e)
        return False
    else:
        if var.empty:
            print("Função de email getDataCheck")
            return False
    return True

def generateInternedDataTableCheck():
    try:
        var = generateInternedDataTable(authentic())
    except Exception as e:
        print(e)
        return False
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
            print("Função de email generateInternedDataTableCheck")
            return False
    return True


def generateCityDataTableCheck():
    try:
        var = generateCityDataTable(authentic())
    except Exception as e:
        print(e)
        return False
    else:
        if ['Município', 
            'Confirmados', 
            'Óbitos', 
            'Incidência',
            'CEP'] != list(var):
            print("Função de email generateCityDataTableCheck")
            return False
    return True

def generateStateDataTableCheck():

    try:
        var = generateStateDataTable(authentic())
    except Exception as e:
        print(e)
        return False
    else:
        if ['Dias',
            'Confirmados',
            'Óbitos'] != list(var):
            print("Função de email generateStateDataTableCheck")
            return False
    return True

def generateComorbidityTableCheck():
    try:
        var = generateComorbidityTable(authentic())
    except Exception as e:
        print(e)
        return False
    else:
        if ['Morbidades',
            'Qtde'] != list(var):
            print("Função de email generateComorbidityTableCheck")
            return False
    return True

def generateAgeRangeTableCheck():
    try:
        var = generateAgeRangeTable(authentic())
    except Exception as e:
        print(e)
        return False
    else:
        if ['Faixa Etária', 
            'Confirmados', 
            'Óbitos'] != list(var):
            print("Função de email  generateAgeRangeTableCheck")
            return False
    return True

def generateGenderTableCheck():
    try:
        var = generateGenderTable(authentic())
    except Exception as e:
        print(e)
        return False
    else:
        if ['Obitos Masculino',
            'Obitos Feminino',
            'Confirmados Masculino',
            'Confirmados Feminino'] != list(var):
            print("Função de email generateGenderTableCheck")
            return False
    return True

def check():
    return authenticCheck() and\
    getDataCheck() and\
    generateInternedDataTableCheck() and\
    generateCityDataTableCheck() and\
    generateStateDataTableCheck() and\
    generateComorbidityTableCheck() and\
    generateAgeRangeTableCheck() and\
    generateGenderTableCheck()