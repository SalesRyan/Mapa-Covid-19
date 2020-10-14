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

    path('som/list/', som_list_view, name='list_som'),
    path('som/detalhes/<int:classe>', som_detalhes_view, name='detalhes_som'),

    path('sobre', sobre_view, name='sobre'),
]
