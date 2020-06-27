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

def atualizarDataUpdate(d):
    if(DataAtualizacao.objects.all().last().data != d[0][0]):
        DataAtualizacao.objects.all().update(
            data = d[0][0]
        )
        return True
    return False

def atualizarDadosEstado(d):
    for line in d[-5:]:    
        DadosEstado.objects.update_or_create(
            data=datetime.strptime(line[0]+'/2020','%d/%m/%Y'),
            defaults={
                'confirmados':line[1],
                'obitos':line[2],
            }   
        )

def atualizarCasosCidade(d):
    for line in d:
        CasosCidade.objects.update_or_create(
            nome=line[0],
            cep=line[4],
            defaults = {
                'confirmados':line[1],
                'obitos':line[2],
                'incidencia':str(line[3]).replace(',','.'),
            }
        )

def atualizarLeitos(d):
    for line in d[-5:]:
        Leitos.objects.update_or_create(
            data=datetime.strptime(line[0],'%d/%m/%Y'),
            defaults={
                'capacidade_clinicos':line[1],
                'ocupados_clinicos':line[2],
                'capacidade_uti':line[3],
                'ocupados_uti':line[4],
                'capacidade_estabilizacao':line[5],
                'ocupados_estabilizacao':line[6],
                'capacidade_respiradores':line[7],
                'ocupados_respiradores':line[8],
                'altas':line[9],
            }
        )
    
def atualizarCasosSexo(d):
    CasosSexo.objects.all().update(
        obitos_masculinos=d[0][0],
        obitos_femininos=d[0][1],
        casos_masculinos=d[0][2],
        casos_femininos=d[0][3],
    )

def atualizarCasosFaixaEtaria(d):
    for line in d:
        CasosFaixaEtaria.objects.all().update_or_create(
            faixa_etaria=line[0],
            defaults= {
                'confirmados':line[1],
                'obitos':line[2],
            }
        )

def atualizarComorbidades(d):
    for line in d:
        Comorbidades.objects.all().update_or_create(
            nome=line[0],
            defaults = {
                'quantidade':line[1]
            }
        )

def verification():
    dfs = check()
    if not True in map(lambda df : df.empty, dfs.values()):
        try:
            if atualizarDataUpdate(dfs['Data'].values):
                atualizarDadosEstado(dfs['DadosEstado'].values)
                atualizarCasosCidade(dfs['CasosCidade'].values)
                atualizarLeitos(dfs['Leitos'].values)
                atualizarCasosSexo(dfs['CasosSexo'].values)
                atualizarCasosFaixaEtaria(dfs['CasosFaixaEtaria'].values)
                atualizarComorbidades(dfs['Comorbidades'].values)
        except Exception as e:
            mail('Exception on atualizar.verification', str(e))
