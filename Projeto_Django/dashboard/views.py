from django.shortcuts import render
import os
from .models import *
from django.core.paginator import Paginator,InvalidPage, EmptyPage
import json
# Create your views here.

def site_view(request):
    env = os.environ
    GOOGLE_API_KEY = env.get('GOOGLE_API_KEY')


    data_atualizacao = DataAtualizacao.objects.all().last()
    dados_estado = DadosEstado.objects.all()
    casos_cidade = CasosCidade.objects.all()
    leitos = Leitos.objects.all()
    casos_sexo = CasosSexo.objects.all().last()
    casos_faixa_etaria = CasosFaixaEtaria.objects.all()
    comorbidades = Comorbidades.objects.all()
    
    size = len(dados_estado)
    obitos_atual = dados_estado.last().obitos
    obitos_novos = obitos_atual - dados_estado[size-2].obitos
    
    confirmados_atual = dados_estado.last().confirmados
    confirmados_novos = confirmados_atual - dados_estado[size-2].confirmados

    data_casos_cidades = {
        'data': [{
            'date':str(obj.data.strftime('%d-%m-%Y')),
            'confirmados':obj.confirmados,
            'obitos':obj.obitos,
        } for obj in dados_estado]
    }

    data_leitos = {
        'data': [{
            'date':str(obj.data.strftime('%d-%m-%Y')),
            'capacidadeClinicos':obj.capacidade_clinicos,
            'ocupadosClinicos':obj.ocupados_clinicos,
            'capacidadeUti':obj.capacidade_uti,
            'ocupadosUti':obj.ocupados_uti,
            'capacidadeEstabilizacao':obj.capacidade_estabilizacao,
            'ocupadosEstabilizacao':obj.ocupados_estabilizacao,
            'capacidadeRespiradores':obj.capacidade_respiradores,
            'ocupadosRespiradores':obj.ocupados_respiradores,
        } for obj in leitos]
    }

    context = {
        'google_api_key': GOOGLE_API_KEY,
        'data_atualizacao': data_atualizacao,
        'dados_estado': dados_estado,
        'confirmados_atual': confirmados_atual,
        'confirmados_novos': confirmados_novos,
        'obitos_atual': obitos_atual,
        'obitos_novos': obitos_novos,
        'casos_cidade': casos_cidade,
        'data_casos_cidade': json.dumps(data_casos_cidades),
        'leitos': leitos,
        'data_leitos': json.dumps(data_leitos),
        'casos_sexo': casos_sexo,
        'casos_faixa_etaria': casos_faixa_etaria,
        'comorbidades': comorbidades,

    }

    return render(request, 'dashboard/index.html', context)

