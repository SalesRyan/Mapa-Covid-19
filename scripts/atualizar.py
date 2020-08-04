from scripts.verificar import check
from dashboard.models import *
import pandas as pd
from datetime import datetime, timedelta
from scripts.email import mail
from unidecode import unidecode
from scripts.funcoes import PredFull, pred_clinical
from django.db.models import Sum



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
            nome=unidecode(str(line[0])),
            defaults = {
                'cep':line[5],
                'confirmados':line[1],
                'obitos':line[2],
                'incidencia':str(line[3]).replace(',','.'),
                'populacao':line[4]
            }
        )

def atualizarCasosRegioes():
    for obj in CasosRegioes.objects.all():
        casos_cidade = CasosCidade.objects.filter(regiao=obj)
        obj.obitos = casos_cidade.aggregate(Sum('obitos'))['obitos__sum']
        obj.confirmados = casos_cidade.aggregate(Sum('confirmados'))['confirmados__sum']
        obj.incidencia = obj.confirmados*10000/(sum([casos.populacao for casos in casos_cidade]))
        obj.save()
    # for obj in CasosRegioes.objects.all():
    #     obj.obitos = CasosCidade.objects.filter(regiao=obj).aggregate(Sum('obitos'))['obitos__sum']
    #     obj.confirmados = CasosCidade.objects.filter(regiao=obj).aggregate(Sum('confirmados'))['confirmados__sum']
    #     obj.save()

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

def atualizarPred(d):
    pred_confirmados = PredFull(d,mode=14,name='Confirmados')
    pred_obitos = PredFull(d,mode=14,name='Óbitos')
    last_date = list(d['Dias'])[-1]
    last_date = datetime.strptime(str(last_date)+'/2020','%d/%m/%Y')
    predicoes = DadosEstadoPredicao.objects.all()

    count = 1
    for ob, conf, obt in zip(predicoes, pred_confirmados, pred_obitos):
        ob.data = last_date+timedelta(days=count)
        ob.confirmados = conf
        ob.obitos = obt
        ob.save()
        count+=1

def atualizarPredLeitos(d):
    pred_leitos = pred_clinical(d,mode=3)
    # pred_obitos = PredFull(df,mode=14,name='Óbitos')
    last_date = list(d['Dias'])[-1]
    last_date = datetime.strptime(str(last_date),'%d/%m/%Y')
    count = 1
    objetos = LeitosPredicao.objects.all()
    for obj, LC, UTI, LE, LR in zip(objetos, pred_leitos['LC'], pred_leitos['UTI'], pred_leitos['LE'], pred_leitos['LR']):
        obj.data=last_date+timedelta(days=count)
        obj.taxa_ocupados_clinicos=LC
        obj.taxa_ocupados_uti=UTI
        obj.taxa_ocupados_estabilizacao=LE
        obj.taxa_ocupados_respiradores=LR
        obj.save()
        count += 1
    
def verification():
    dfs = check()
    if not True in map(lambda df : df.empty, dfs.values()):
        # try:
        if atualizarDataUpdate(dfs['Data'].values):
            atualizarDadosEstado(dfs['DadosEstado'].values)
            atualizarCasosCidade(dfs['CasosCidade'].values)
            atualizarLeitos(dfs['Leitos'].values)
            atualizarCasosSexo(dfs['CasosSexo'].values)
            atualizarCasosFaixaEtaria(dfs['CasosFaixaEtaria'].values)
            atualizarComorbidades(dfs['Comorbidades'].values)
            atualizarPred(dfs['DadosEstado'])
            atualizarPredLeitos(dfs['Leitos'])
            atualizarCasosRegioes()
        # except Exception as e:
        #     mail('Exception on atualizar.verification', str(e))
