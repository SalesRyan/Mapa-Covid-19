from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', site_view, name='site'),
    path('regioes/detalhes/<str:nome>', detalhes_view, name='detalhes_regiao'),
    path('regioes/list', regiao_list_view, name='list_regioes'),

    path('cidades/detalhes/<str:nome>', detalhes_cidade_view, name='detalhes_cidade'),
    path('cidades/list', cidades_list_view, name='list_cidades'),

    path('agrupamento/list/', agrupamento_list_view, name='list_agrupamento'),
    path('agrupamento/detalhes/<int:classe>', agrupamento_detalhes_view, name='detalhes_agrupamento'),

    path('api/poligonos/regioes', poligonos_regioes_api_view, name='api_poligonos_regioes'),
    path('api/grafico/cidades', grafico_cidades_api_view, name='api_grafico_cidades'),
    path('api/grafico/leitos', grafico_leitos_api_view, name='api_grafico_leitos'),
    path('api/grafico/comorbidades', grafico_comormidades_api_view, name='api_grafico_comorbidades'),
    path('api/grafico/sexo/confirmados', grafico_sexo_confirmados_api_view, name='api_grafico_sexo_confirmados'),
    path('api/grafico/sexo/obitos', grafico_sexo_obitos_api_view, name='api_grafico_sexo_obitos'),
    path('api/grafico/faixa-etaria', grafico_faixa_api_view, name='api_grafico_faixa'),

    path('sobre', sobre_view, name='sobre'),
]
