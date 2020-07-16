from django.shortcuts import render
import os
from .models import *
from django.core.paginator import Paginator,InvalidPage, EmptyPage
import json
from django.db.models import Max,Sum
# Create your views here.



def site_view(request):
    env = os.environ
    GOOGLE_API_KEY = env.get('GOOGLE_API_KEY')

    data_atualizacao = DataAtualizacao.objects.last()
    dados_estado = DadosEstado.objects.all()
    casos_cidade = CasosCidade.objects.all()
    leitos = Leitos.objects.all()
    casos_sexo = CasosSexo.objects.all().last()
    casos_faixa_etaria = CasosFaixaEtaria.objects.all()
    comorbidades = Comorbidades.objects.all()
    dados_estado_pred = DadosEstadoPredicao.objects.all()
    dados_leitos_pred = LeitosPredicao.objects.all()
    
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


    data_comorbidades = {
        'data': [{
            'name':obj.nome,
            'value':obj.quantidade,
        } for obj in comorbidades]
    } 
    data_sexo_casos = {
        'data' : [{
                'label':'Masculino',
                'value':casos_sexo.casos_masculinos,
            },{
                'label':'Feminino',
                'value':casos_sexo.casos_femininos
            }]
    }
    data_sexo_obitos = {
        'data' : [{
                'label':'Masculino',
                'value':casos_sexo.obitos_masculinos,
            },{
                'label':'Feminino',
                'value':casos_sexo.obitos_femininos,
            }]
    }
    data_faixa = {
        'data': [{
            'faixaEtaria':obj.faixa_etaria,
            'confirmados':obj.confirmados,
            'obitos':obj.obitos,
        } for obj in casos_faixa_etaria]
    }
    referencia = casos_cidade.aggregate(Max('incidencia'))['incidencia__max']
   
    def prepareJson(objeto):
        return {
            "nome": objeto.nome,
            "obitos": objeto.obitos,
            "confirmados": objeto.confirmados,
            "incidencia": objeto.incidencia,
            "classe": int(objeto.incidencia*10/(2*referencia)),
            "coordenadas": [{
                "lng":float(coordenadas.split(',')[0]),
                "lat":float(coordenadas.split(',')[1])
            }  for coordenadas in objeto.coordenadas.split(' ')]
        }
    
    data_mapa = {
        'data': [prepareJson(obj) for obj in casos_cidade]
    }

    """ sum_object = leitos.aggregate(Sum('capacidade_clinicos'),
        Sum('capacidade_uti'),
        Sum('capacidade_estabilizacao'),
        Sum('capacidade_respiradores'),
        Sum('ocupados_clinicos'),
        Sum('ocupados_uti'),
        Sum('ocupados_estabilizacao'),
        Sum('ocupados_respiradores')
    )

    capacidade = sum_object['capacidade_clinicos__sum']
    capacidade += sum_object['capacidade_uti__sum']
    capacidade += sum_object['capacidade_estabilizacao__sum']
    capacidade += sum_object['capacidade_respiradores__sum']
    
    ocupacao = sum_object['ocupados_clinicos__sum']
    ocupacao += sum_object['ocupados_uti__sum']
    ocupacao += sum_object['ocupados_estabilizacao__sum']
    ocupacao += sum_object['ocupados_respiradores__sum'] """

    


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
    

    context = {
        'google_api_key': GOOGLE_API_KEY,
        'data_atualizacao': data_atualizacao,
        'confirmados_atual': confirmados_atual,
        'confirmados_novos': confirmados_novos,
        'obitos_atual': obitos_atual,
        'obitos_novos': obitos_novos,
        'data_faixa':json.dumps(data_faixa),
        'data_sexo_casos':json.dumps(data_sexo_casos),
        'data_sexo_obitos':json.dumps(data_sexo_obitos),
        'data_casos_cidade': json.dumps(data_casos_cidades),
        'data_leitos': json.dumps(data_leitos),
        'data_comorbidades': json.dumps(data_comorbidades),
        'casos_cidade': casos_cidade,
        'data_mapa': json.dumps(data_mapa),
        'ocupacao_atual':str(round(taxa_ocupacao,2)),
        'ocupacao_novos':taxa_ocupacao_penult,
        'altas_atual':altas_atual,
        'altas_novos':altas_novos,
    }

    return render(request, 'dashboard/index.html', context)
