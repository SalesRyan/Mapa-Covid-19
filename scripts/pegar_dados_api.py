import pandas as pd
import numpy as np

import requests
import time
from datetime import datetime, timedelta, date

from ast import literal_eval
import json
import pandas as pd
import numpy as np

from dashboard.models import *
from unidecode import unidecode


import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)

env = os.environ
key_ae = env.get('key_ae')
key_bf = env.get('key_bf')
key_bpc = env.get('key_bpc')

df = pd.read_excel('arquivos_auxiliares/Extração de dados/cidades.xlsx')
codigos = df['Codigo'].to_list()
nomes_cidades = df['Município [-]'].to_list()


cod_teresina = '2211001'
data_atual = date.today()
mes_ano = None

nomes = ['bpc-por-municipio', 'bolsa-familia-por-municipio', 'auxilio-emergencial-por-municipio']
headers_ae = {'Accept': 'application/json', 'chave-api-dados': key_ae}
headers_bf = {'Accept': 'application/json', 'chave-api-dados': key_bf}
headers_bpc = {'Accept': 'application/json', 'chave-api-dados': key_bpc}

while mes_ano is None:
    ano = data_atual.year
    mes = data_atual.month
    if mes < 10:
        mes = '0' + str(mes)
    atual_mes_ano = str(ano) + str(mes)
    url = f'http://www.portaltransparencia.gov.br/api-de-dados/auxilio-emergencial-por-municipio?mesAno={atual_mes_ano}&codigoIbge={cod_teresina}&pagina=1'
    time.sleep(0.1)
    r = requests.get(url, headers = headers_ae)
    if r.text == '[]':
        data_atual = data_atual - timedelta(days = 31 )
    else:
        mes_ano = atual_mes_ano



for cod,nome in zip(codigos,nomes_cidades):
    url_ae = f'http://www.portaltransparencia.gov.br/api-de-dados/{nomes[0]}?mesAno={mes_ano}&codigoIbge={cod}&pagina=1'
    url_bf = f'http://www.portaltransparencia.gov.br/api-de-dados/{nomes[1]}?mesAno={mes_ano}&codigoIbge={cod}&pagina=1'
    url_bpc = f'http://www.portaltransparencia.gov.br/api-de-dados/{nomes[2]}?mesAno={mes_ano}&codigoIbge={cod}&pagina=1'
    
    time.sleep(0.1)
    response_ae = requests.get(url_ae, headers = headers_ae)
    time.sleep(0.1)
    response_bf = requests.get(url_bf, headers = headers_bf)
    time.sleep(0.1)
    response_bpc = requests.get(url_bpc, headers = headers_bpc)
    time.sleep(0.1)

    dados_dicio_bf = literal_eval(response_bf.text)
    dados_dicio_ae = literal_eval(response_ae.text)
    dados_dicio_bpc = literal_eval(response_bpc.text)

    dicio_zero = {
        'valor':0,
        'quantidadeBeneficiados':0,
    }

    if len(dados_dicio_bf) == 0:
        dados_dicio_bf = dicio_zero
    else:
        dados_dicio_bf = dados_dicio_bf[0]
    
    if len(dados_dicio_ae) == 0:
        dados_dicio_ae = dicio_zero
    else:
        dados_dicio_ae = dados_dicio_ae[0]
    
    if len(dados_dicio_bpc) == 0:
        dados_dicio_bpc = dicio_zero
    else:
        dados_dicio_bpc = dados_dicio_bpc[0]

    cidade = CasosCidade.objects.get(nome=unidecode(nome).upper().replace("'",""))
    print(cidade)

    DadosFinanceiros.objects.update_or_create(
        cidade=cidade,
        defaults={
            'data_atualizacao':data_atual,
            'valor_bolsa_familia':dados_dicio_ae['valor'],
            'quantidade_bolsa_familia':dados_dicio_ae['quantidadeBeneficiados'],
            'valor_auxilio_emergencial':dados_dicio_bf['valor'],
            'quantidade_auxilio_emergencial':dados_dicio_bf['quantidadeBeneficiados'],
            'valor_BPC':dados_dicio_bpc['valor'],
            'quantidade_BPC':dados_dicio_bpc['quantidadeBeneficiados'],
        }   
    )        
    time.sleep(2)

