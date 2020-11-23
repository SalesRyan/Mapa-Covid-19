from django.shortcuts import render
import os
from .models import *
from django.core.paginator import Paginator,InvalidPage, EmptyPage
import json
from django.db.models import Max,Sum
from scripts.funcoes import propDoen, respSaude
import pandas as pd
from ast import literal_eval
import numpy as np

from django.http import JsonResponse

from .functions import *

# Create your views here.



def site_view(request):
    env = os.environ
    GOOGLE_API_KEY = env.get('GOOGLE_API_KEY')

    data_atualizacao = DataAtualizacao.objects.last()
    dados_estado = DadosEstado.objects.all()
    casos_cidade = CasosCidade.objects.values("nome","confirmados","obitos","incidencia","coordenadas","regiao__nome","classe")
    leitos = Leitos.objects.all().order_by("data")
    casos_sexo = CasosSexo.objects.all().last()
    casos_faixa_etaria = CasosFaixaEtaria.objects.all()
    comorbidades = Comorbidades.objects.all()
    dados_estado_pred = DadosEstadoPredicao.objects.all()
    dados_leitos_pred = LeitosPredicao.objects.all()
    casos_regioes = CasosRegioes.objects.all().values()
    recuperados = Recuperados.objects.last().quantidade
    piaui = json.dumps({'data':literal_eval(PoligonoPI.objects.last().poligono)})
    
    size = len(dados_estado)
    obitos_atual = dados_estado.last().obitos
    obitos_novos = obitos_atual - dados_estado[size-2].obitos
    confirmados_atual = dados_estado.last().confirmados
    confirmados_novos = confirmados_atual - dados_estado[size-2].confirmados
    
    size_leitos = len(leitos)
    last_leitos = leitos.last()
    penult_leitos = leitos[size_leitos-2]
    altas_atual = last_leitos.altas
    altas_novos = altas_atual - penult_leitos.altas
    referencia = casos_cidade.aggregate(Max('incidencia'))['incidencia__max']
    num_classe_som = casos_cidade.aggregate(Max('classe'))['classe__max']
   
    referencia_regioes = casos_regioes.aggregate(Max('incidencia'))['incidencia__max']
    
    data_mapa = {
        'data': [prepareJson(obj,referencia) for obj in casos_cidade]
    }
    
    data_mapa_regioes = {
        'data': [prepareRegioesJson(obj,referencia_regioes) for obj in casos_regioes]
    }

    incidencia_cidades = data_min_max(data_mapa['data'])
    incidencia_regioes = data_min_max(data_mapa_regioes['data'])

    ocupacao = last_leitos.ocupados_clinicos
    ocupacao += last_leitos.ocupados_uti
    ocupacao += last_leitos.ocupados_estabilizacao
    ocupacao += last_leitos.ocupados_respiradores
    
    capacidade = last_leitos.capacidade_clinicos
    capacidade += last_leitos.capacidade_uti
    capacidade += last_leitos.capacidade_estabilizacao
    capacidade += last_leitos.capacidade_respiradores
    
    taxa_ocupacao = (ocupacao*100)/capacidade

    ocupacao_penult = penult_leitos.ocupados_clinicos
    ocupacao_penult += penult_leitos.ocupados_uti
    ocupacao_penult += penult_leitos.ocupados_estabilizacao
    ocupacao_penult += penult_leitos.ocupados_respiradores
    
    capacidade_penult = penult_leitos.capacidade_clinicos
    capacidade_penult += penult_leitos.capacidade_uti
    capacidade_penult += penult_leitos.capacidade_estabilizacao
    capacidade_penult += penult_leitos.capacidade_respiradores

    taxa_ocupacao_penult = (ocupacao_penult*100)/capacidade_penult
    taxa_ocupacao_penult = taxa_ocupacao-taxa_ocupacao_penult

    if taxa_ocupacao_penult>=0:
        taxa_ocupacao_penult = '+'+str(round(taxa_ocupacao_penult,2))
    else:
        taxa_ocupacao_penult = str(round(taxa_ocupacao_penult,2))
    
    dados_estado_list = list(dados_estado.values("confirmados", "obitos"))
    confirmados = []
    obitos = []

    for dados_estado_dict in dados_estado_list:
        confirmados.append(dados_estado_dict['confirmados'])
        obitos.append(dados_estado_dict['obitos'])
    dados_estado_dict = {
        'confirmados':confirmados,
        'obitos':obitos,
    }
    dados_estado_dict = pd.DataFrame.from_dict(dados_estado_dict)
    
    leitos_list = list(leitos.values("ocupados_clinicos", "ocupados_uti","ocupados_estabilizacao","ocupados_respiradores","altas", "capacidade_uti", "capacidade_respiradores", "capacidade_clinicos"))
    
    ocupados_clinicos = []
    ocupados_uti = []
    ocupados_estabilizacao = []
    ocupados_respiradores = []
    altas = []
    capacidade_uti = []
    capacidade_clinicos = []
    capacidade_respiradores = []

    for leitos_dict in leitos_list:
        ocupados_clinicos.append(leitos_dict['ocupados_clinicos'])
        ocupados_uti.append(leitos_dict['ocupados_uti'])
        ocupados_estabilizacao.append(leitos_dict['ocupados_estabilizacao'])
        ocupados_respiradores.append(leitos_dict['ocupados_respiradores'])
        altas.append(leitos_dict['altas'])
        capacidade_uti.append(leitos_dict['capacidade_uti'])
        capacidade_clinicos.append(leitos_dict['capacidade_clinicos'])
        capacidade_respiradores.append(leitos_dict['capacidade_respiradores'])

    leitos_dict = {
        'ocupados_clinicos':ocupados_clinicos,
        'ocupados_uti':ocupados_uti,
        'ocupados_estabilizacao':ocupados_estabilizacao,
        'ocupados_respiradores':ocupados_respiradores,
        'altas':altas,
        'capacidade_uti':capacidade_uti,
        'capacidade_clinicos':capacidade_clinicos,
        'capacidade_respiradores':capacidade_respiradores
    }
    leitos_dict = pd.DataFrame.from_dict(leitos_dict)
    
    prop_doen = round(propDoen(leitos_dict, dados_estado_dict),2)
    resp_saude = round(respSaude(leitos_dict),2)
    
    quantidade_confirmados = casos_cidade.exclude(confirmados=0).count()
    quantidade_obitos = casos_cidade.exclude(obitos=0).count()

    percentual_confirmados = quantidade_confirmados/224
    percentual_obitos = quantidade_obitos/224


    context = {
        'google_api_key': GOOGLE_API_KEY,
        'data_atualizacao': data_atualizacao,
        'confirmados_atual': confirmados_atual,
        'confirmados_novos': confirmados_novos,
        'obitos_atual': obitos_atual,
        'obitos_novos': obitos_novos,
        'casos_cidade': casos_cidade,
        'data_mapa': json.dumps(data_mapa),
        'data_mapa_regioes': json.dumps(data_mapa_regioes),
        'ocupacao_atual':str(round(taxa_ocupacao,2)).replace('.', ','),
        'ocupacao_novos':str(taxa_ocupacao_penult).replace('.', ','),
        'incidencia_cidades':incidencia_cidades,
        'incidencia_regioes':incidencia_regioes,
        'recuperados':recuperados,
        'prop_doen':prop_doen,
        'resp_saude':resp_saude,
        'percentual_confirmados':percentual_confirmados,
        'percentual_obitos':percentual_obitos,
        'num_classe_som':num_classe_som,
        'piaui':piaui
    }
    
    return render(request, 'dashboard/index.html', context)

def detalhes_view(request, nome):
    data_atualizacao = DataAtualizacao.objects.last()
    casos_regioes = HistoricoDiario.objects.get(regiao__nome=nome)
    casos_cidade = CasosCidade.objects.filter(regiao=casos_regioes.regiao).values("nome","confirmados","obitos","incidencia","regiao")
    casos_regioes_pred = HistoricoDiarioPred.objects.get(regiao__nome=nome)

    dados_pred = literal_eval(casos_regioes_pred.dados)
    dados = literal_eval(casos_regioes.dados)
    data_historico_diario = {
        'data': [{
            'date':obj[0],
            'confirmados':obj[1],
            'obitos':obj[2],
        } for obj in dados]
    }
    confirmados_atual = data_historico_diario['data'][-1]['confirmados']
    confirmados_novos = int(confirmados_atual) - int(data_historico_diario['data'][-2]['confirmados'])
    obitos_atual = data_historico_diario['data'][-1]['obitos']
    obitos_novos = int(obitos_atual) - int(data_historico_diario['data'][-2]['obitos'])
    data_historico_diario['data'][-1]['lineDash'] = '2,2'
    for dia in dados_pred:
        data_historico_diario['data'].append({
            'date':dia[0],
            'confirmados':dia[1],
            'obitos':dia[2],
            'additional': '(Projeção)',
            'lineColor': '#f8cd3c',
            'lineDash': '2,2',
        })


    context = {
        'confirmados_atual':confirmados_atual,
        'confirmados_novos':confirmados_novos,
        'obitos_atual':obitos_atual,
        'obitos_novos':obitos_novos,
        'data_historico_diario':json.dumps(data_historico_diario),
        'casos_cidade':casos_cidade,
        'nome':casos_regioes.regiao.nome,
        'data_atualizacao':data_atualizacao,
    }
    return render(request, 'regioes/detalhes.html',context)

def regiao_list_view(request):
    regioes = CasosRegioes.objects.all()

    context = {
        'regioes':regioes
    }
    
    return render(request, 'regioes/list.html', context)

def detalhes_cidade_view(request, nome):
    data_atualizacao = DataAtualizacao.objects.last()
    detalhe_cidade = HistoricoCidadesDiario.objects.get(cidade__nome=nome)
    casos_regioes_pred = HistoricoCidadesDiarioPred.objects.get(cidade__nome=nome)


    dados = literal_eval(detalhe_cidade.dados)
    dados_pred = literal_eval(casos_regioes_pred.dados)
    data_historico_diario = {
        'data': [{
            'date':obj[0],
            'confirmados':obj[1],
            'obitos':obj[2],
        } for obj in dados]
    }
    confirmados_atual = data_historico_diario['data'][-1]['confirmados']
    confirmados_novos = int(confirmados_atual) - int(data_historico_diario['data'][-2]['confirmados'])
    obitos_atual = data_historico_diario['data'][-1]['obitos']
    obitos_novos = int(obitos_atual) - int(data_historico_diario['data'][-2]['obitos'])

    data_historico_diario['data'][-1]['lineDash'] = '2,2'
    for dia in dados_pred:
        data_historico_diario['data'].append({
            'date':dia[0],
            'confirmados':dia[1],
            'obitos':dia[2],
            'additional': '(Projeção)',
            'lineColor': '#f8cd3c',
            'lineDash': '2,2',
        })


    context = {
        'confirmados_atual':confirmados_atual,
        'confirmados_novos':confirmados_novos,
        'obitos_atual':obitos_atual,
        'obitos_novos':obitos_novos,
        'data_historico_diario':json.dumps(data_historico_diario),
        'nome':detalhe_cidade.cidade.nome,
        'data_atualizacao':data_atualizacao,
    }
    return render(request, 'cidades/detalhes.html',context)

def cidades_list_view(request):
    cidades = CasosCidade.objects.all()

    context = {
        'cidades':cidades
    }
    
    return render(request, 'cidades/list.html', context)

def sobre_view(request):
    return render(request, 'dashboard/sobre.html')

def agrupamento_list_view(request):
    cidades = CasosCidade.objects.all()
    num_classe_som = cidades.aggregate(Max('classe'))['classe__max']


    context = {
        'classe':[num for num in range(num_classe_som+1)],
        'cor':['#67ad45','#f20089','#ff0000']
    }
    
    return render(request, 'som/list.html', context)


def agrupamento_detalhes_view(request, classe):
    env = os.environ
    GOOGLE_API_KEY = env.get('GOOGLE_API_KEY')
    data_atualizacao = DataAtualizacao.objects.last()
    historico_cidades = HistoricoCidadesDiario.objects.filter(cidade__classe=classe)
    # casos_cidade = historico_cidades.values("cidade__nome")
    casos_cidade = CasosCidade.objects.filter(classe=classe).values("nome","confirmados","obitos","incidencia","regiao","classe","coordenadas","populacao")

    
    referencia = casos_cidade.aggregate(Max('incidencia'))['incidencia__max']
    pop_total = casos_cidade.aggregate(Sum('populacao'))['populacao__sum']
    conf_total = casos_cidade.aggregate(Sum('confirmados'))['confirmados__sum']
    incidencia = conf_total/pop_total * 10000
    def prepareJson(objeto):
        return {
            "nome": objeto['nome'],
            "obitos": objeto['obitos'],
            "confirmados": objeto['confirmados'],
            "incidencia": str(objeto['incidencia']).replace('.',','),
            "classeSom": objeto['classe'],
            "classe": int(objeto['incidencia']*10/(2*referencia)),
            "coordenadas": [{
                "lng":float(coordenadas.split(',')[0]),
                "lat":float(coordenadas.split(',')[1])
            }  for coordenadas in objeto['coordenadas'].split(' ')]
        }

    confirmados_list = list(map(lambda x: x['confirmados'], casos_cidade))
    obitos_list = list(map(lambda x: x['obitos'], casos_cidade))
    incidencia_list = list(map(lambda x: x['incidencia'], casos_cidade))

    confirmados_media = np.average(confirmados_list)
    obitos_media = np.average(obitos_list)
    incidencia_media = np.average(incidencia_list)
    confirmados_desvio = np.std(confirmados_list)
    obitos_desvio = np.std(obitos_list)
    incidencia_desvio = np.std(incidencia_list)

    df = pd.read_csv("arquivos_auxiliares/Extração de dados/final.csv")
    df_pop = pd.read_csv("arquivos_auxiliares/Extração de dados/final_normalizado.csv")

    # media_bpc = np.average(dados_financeiros['VALOR_BPC'])
    df_filter = pd.concat([df[df['MUNICIPIO'] == obj['nome']] for obj in casos_cidade])
    df_filter_pop = pd.concat([df_pop[df_pop['MUNICIPIO'] == obj['nome']] for obj in casos_cidade])
    bpc_desvio = round(df_filter_pop['VALOR_BPC'].std(),2)
    ae_desvio =  round(df_filter_pop['VALOR_AE'].std(),2)
    bf_desvio =  round(df_filter_pop['VALOR_BF'].std(),2)
    
    bpc_media = round(df_filter_pop['VALOR_BPC'].mean(),2)
    ae_media =  round(df_filter_pop['VALOR_AE'].mean(),2)
    bf_media =  round(df_filter_pop['VALOR_BF'].mean(),2)

    bpc_qtd = round(df_filter['QTD_BPC'].sum()/pop_total,2)
    ae_qtd =  round(df_filter['QTD_AE'].sum()/pop_total,2)
    bf_qtd =  round(df_filter['QTD_BF'].sum()/pop_total,2)


    data_mapa = {
        'data': [prepareJson(obj) for obj in casos_cidade]
    }

    context = {
        'google_api_key':GOOGLE_API_KEY,
        'piaui':json.dumps({'data':literal_eval(PoligonoPI.objects.last().poligono)}),
        'data_mapa':json.dumps(data_mapa),
        'casos_cidade':casos_cidade,
        'nome':classe,
        'data_atualizacao':data_atualizacao,
        'bpc_desvio':bpc_desvio,
        'ae_desvio':ae_desvio,
        'bf_desvio':bf_desvio,
        'bpc_media':bpc_media,
        'ae_media':ae_media,
        'bf_media':bf_media,
        'bpc_qtd':bpc_qtd,
        'ae_qtd':ae_qtd,
        'bf_qtd':bf_qtd,
        'confirmados':round(np.sum(confirmados_list), 4),
        'obitos':round(np.sum(obitos_list), 4),
        'incidencia':round(incidencia,2),
        'confirmados_media':round(confirmados_media, 2),
        'obitos_media':round(obitos_media, 2),
        'incidencia_media':round(incidencia_media, 2),
        'confirmados_desvio':round(confirmados_desvio),
        'obitos_desvio':round(obitos_desvio, 2),
        'incidencia_desvio':round(incidencia_desvio, 2),
    }
    return render(request, 'som/detalhes.html',context)

def poligonos_regioes_api_view(request):
    casos_regioes = CasosRegioes.objects.all().values()
    referencia_regioes = casos_regioes.aggregate(Max('incidencia'))['incidencia__max']
    
    data_mapa_regioes = {
        'data': [prepareRegioesJson(obj,referencia_regioes) for obj in casos_regioes]
    }
    return JsonResponse(data_mapa_regioes)

def grafico_cidades_api_view(request):
    dados_estado = DadosEstado.objects.all()
    dados_estado_pred = DadosEstadoPredicao.objects.all()
    data_casos_cidades = {
            'data': [{
                'date':str(obj.data.strftime('%d-%m-%Y')),
                'confirmados':obj.confirmados,
                'obitos':obj.obitos, 
            } for obj in dados_estado]
        }
    data_casos_cidades['data'][-1]['lineDash'] = '2,2'
    for obj in dados_estado_pred:
        data_casos_cidades['data'].append({
            'date':str(obj.data.strftime('%d-%m-%Y')),
            'confirmados':obj.confirmados,
            'obitos':obj.obitos,
            'additional': '(Projeção)',
            'lineColor': '#f8cd3c',
            'lineDash': '2,2',
        })
    return JsonResponse(data_casos_cidades)

def grafico_leitos_api_view(request):
    leitos = Leitos.objects.all().order_by("data")
    dados_leitos_pred = LeitosPredicao.objects.all()

    data_leitos = {
        'data': [{
            'date':str(obj.data.strftime('%d-%m-%Y')),
            'capacidadeClinicos':obj.capacidade_clinicos,
            'ocupadosClinicos':obj.ocupados_clinicos/obj.capacidade_clinicos,
            'capacidadeUti':obj.capacidade_uti,
            'ocupadosUti':obj.ocupados_uti/obj.capacidade_uti,
            'capacidadeEstabilizacao':obj.capacidade_estabilizacao,
            'ocupadosEstabilizacao':obj.ocupados_estabilizacao/obj.capacidade_estabilizacao,
            'capacidadeRespiradores':obj.capacidade_respiradores,
            'ocupadosRespiradores':obj.ocupados_respiradores/obj.capacidade_respiradores,
        } for obj in leitos]
    }

    data_leitos['data'][-1]['lineDash'] = '2,2'
    for obj in dados_leitos_pred:
        data_leitos['data'].append({
            'date':str(obj.data.strftime('%d-%m-%Y')),
            'capacidadeClinicos':1,
            'ocupadosClinicos':obj.taxa_ocupados_clinicos/100,
            'capacidadeUti':1,
            'ocupadosUti':obj.taxa_ocupados_uti/100,
            'capacidadeEstabilizacao':1,
            'ocupadosEstabilizacao':obj.taxa_ocupados_estabilizacao/100,
            'capacidadeRespiradores':1,
            'ocupadosRespiradores':obj.taxa_ocupados_respiradores/100,
            'additional': '(Projeção)',
            'lineColor': '#f8cd3c',
            'lineDash': '2,2',
        })
    return JsonResponse(data_leitos)

def grafico_comormidades_api_view(request):
    comorbidades = Comorbidades.objects.all()
    data_comorbidades = {
            'data': [{
                'name':obj.nome,
                'value':obj.quantidade,
            } for obj in comorbidades]
        } 
    return JsonResponse(data_comorbidades)

def grafico_sexo_confirmados_api_view(request):
    casos_sexo = CasosSexo.objects.last()
    data_sexo_casos = {
        'data' : [{
                'label':'Masculino',
                'value':casos_sexo.casos_masculinos,
            },{
                'label':'Feminino',
                'value':casos_sexo.casos_femininos
            }]
    }
    return JsonResponse(data_sexo_casos)

def grafico_sexo_obitos_api_view(request):
    casos_sexo = CasosSexo.objects.last()
    data_sexo_obitos = {
        'data' : [{
                'label':'Masculino',
                'value':casos_sexo.obitos_masculinos,
            },{
                'label':'Feminino',
                'value':casos_sexo.obitos_femininos,
            }]
    }
    return JsonResponse(data_sexo_obitos)

def grafico_faixa_api_view(request):
    casos_faixa_etaria = CasosFaixaEtaria.objects.all()
    data_faixa = {
        'data': [{
            'faixaEtaria':obj.faixa_etaria,
            'confirmados':obj.confirmados,
            'obitos':obj.obitos,
        } for obj in casos_faixa_etaria]
    }
    return JsonResponse(data_faixa)
