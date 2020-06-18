from scripts.Verificar import check
from dashboard.models import *
import pandas as pd
from datetime import datetime
""" 
'Leitos':generateInternedDataTableCheck(sheets),
'CasosCidade':generateCityDataTableCheck(sheets),
'DadosEstado':generateStateDataTableCheck(sheets),
'Comorbidades':generateComorbidityTableCheck(sheets),
'CasosFaixaEtaria':generateAgeRangeTableCheck(sheets),
'CasosSexo':generateGenderTableCheck(sheets)
"""

def atualizarDadosEstado(d): #SUPIMPA
    print(d,"\n")
    return 0
    ob = DadosEstado.objects.update_or_create(
        data=datetime.strptime(d[-1][0],'%d/%m/2020'),
        defaults={
            'confirmados':d[-1][1],
            'obitos':d[-1][2],
        }
    )
    ob.save()

def atualizarCasosCidade(d):
    print(d,"\n")
    return 0
    ob = CasosSexo.objects.all().last()
    ob.update(
        nome=d[0][0],
        confirmados=d[0][1],
        obitos=d[0][2],
        incidencia=d[0][3],
        cep=d[0][4],
    )
    ob.save()

def atualizarLeitos(d): #SUPIMPA(MAIS OU MENOS)
    print(d,"\n")
    return 0
    ob = DadosEstado.objects.update_or_create(
        data=datetime.strptime(d[-1][0],'%d/%m/%Y'),
        defaults={
            'capacidade_clinicos':d[-1][1],
            'ocupados_clinicos':d[-1][2],
            'capacidade_uti':d[-1][3],
            'ocupados_uti':d[-1][4],
            'capacidade_estabilizacao':d[-1][5],
            'ocupados_estabilizacao':d[-1][6],
            'capacidade_respiradores':d[-1][7],
            'ocupados_respiradores':d[-1][8],
            'altas':d[-1][9],
        }
    )
    ob.save()

def atualizarCasosSexo(d): #SUPIMPA
    print(d,"\n")
    return 0
    ob = CasosSexo.objects.all().last()
    ob.update(
        obitos_masculinos=d[0][0],
        obitos_femininos=d[0][1],
        casos_masculinos=d[0][2],
        casos_femininos=d[0][3],
    ) 
    ob.save()

def atualizarCasosFaixaEtaria(d):
    print(d,"\n")
    return 0
    for line in d:
        ob = CasosFaixaEtaria.objects.get(faixa_etaria=line[0]).update(
            confirmados=line[1],
            obitos=line[2],
        )
        ob.save()

def atualizarComorbidades(d):
    print(d,"\n")
    return 0
    for line in d:
        ob = CasosSexo.Comorbidades.objects.get(nome=line[0]).update(
            quantidade=line[1],
        )
        ob.save()

def verification():
    dfs = check()

    if not True in map(lambda df : df.empty, dfs.values()):
        atualizarDadosEstado(dfs['DadosEstado'].values)
        # atualizarCasosCidade(dfs['CasosCidade'].values)
        # atualizarLeitos(dfs['Leitos'].values)
        # atualizarCasosSexo(dfs['CasosSexo'].values)
        # atualizarCasosFaixaEtaria(dfs['CasosFaixaEtaria'].values)
        # atualizarComorbidades(dfs['Comorbidades'].values)

verification() 