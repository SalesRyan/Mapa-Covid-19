from django.shortcuts import render
import os
from .models import *
from django.core.paginator import Paginator,InvalidPage, EmptyPage
import json
# Create your views here.

def site_view(request):
    env = os.environ
    GOOGLE_API_KEY = env.get('GOOGLE_API_KEY')


    data_atualizacao = DataAtualizacao.objects.all()
    dados_estado = DadosEstado.objects.all()
    casos_cidade = CasosCidade.objects.all()
    leitos = Leitos.objects.all()
    casos_sexo = CasosSexo.objects.all()
    casos_faixa_etaria = CasosFaixaEtaria.objects.all()
    comorbidades = Comorbidades.objects.all()
    
    labels = [str(obj.data.strftime('%d/%m')) for obj in dados_estado]
    data = [obj.confirmados for obj in dados_estado]

    context = {
        'google_api_key': GOOGLE_API_KEY,
        'data_atualizacao': data_atualizacao,
        'dados_estado': dados_estado,
        'casos_cidade': casos_cidade,
        'data_casos_cidade': json.dumps({
            'labels':labels[-30:],
            'data':data[-30:],
        }),
        'leitos': leitos,
        'casos_sexo': casos_sexo,
        'casos_faixa_etaria': casos_faixa_etaria,
        'comorbidades': comorbidades,
    }

    return render(request, 'dashboard/index.html', context)


