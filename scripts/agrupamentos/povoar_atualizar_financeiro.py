import pandas as pd
import numpy as np

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

from scripts.agrupamentos.funcoes import *
from scripts.agrupamentos.agrupamentos import definirGrupo
from dashboard.models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)
env = os.environ
key = env.get('key')


cod_teresina = '2211001'
data_atual = date.today()

nomes = ['auxilio-emergencial-por-municipio', 'bolsa-familia-por-municipio', 'bpc-por-municipio']
headers = {'Accept': 'application/json', 'chave-api-dados': key}

mes_ano = min_data(data_atual,headers,nomes,cod_teresina)
print("mes_ano:",mes_ano)
def inserir():

    df = pd.read_excel('arquivos_auxiliares/Extração de dados/cidades.xlsx')
    codigos = df['Codigo'].to_list()
    nomes_cidades = df['Município [-]'].to_list()
    hora = datetime.now().hour

    for cod,nome in zip(codigos,nomes_cidades):
        url_ae = f'http://api.portaldatransparencia.gov.br/api-de-dados/{nomes[0]}?mesAno={mes_ano}&codigoIbge={cod}&pagina=1'
        url_bf = f'http://api.portaldatransparencia.gov.br/api-de-dados/{nomes[1]}?mesAno={mes_ano}&codigoIbge={cod}&pagina=1'
        url_bpc = f'http://api.portaldatransparencia.gov.br/api-de-dados/{nomes[2]}?mesAno={mes_ano}&codigoIbge={cod}&pagina=1'
        
        time.sleep(3)
        dados_dicio_ae = get_data_api(url_ae, headers = headers)
        dados_dicio_bf = get_data_api(url_bf, headers = headers)
        dados_dicio_bpc = get_data_api(url_bpc, headers = headers)

        cidade = CasosCidade.objects.get(nome=unidecode(nome).upper().replace("'",""))
        print("Povoando dados da cidade: ",cidade)
        DadosFinanceiros.objects.update_or_create(
            cidade=cidade,
            defaults={
                'valor_auxilio_emergencial':dados_dicio_ae['valor'],
                'quantidade_auxilio_emergencial':dados_dicio_ae['quantidadeBeneficiados'],
                'valor_bolsa_familia':dados_dicio_bf['valor'],
                'quantidade_bolsa_familia':dados_dicio_bf['quantidadeBeneficiados'],
                'valor_BPC':dados_dicio_bpc['valor'],
                'quantidade_BPC':dados_dicio_bpc['quantidadeBeneficiados'],
            }   
        )

referencia = RefereciaAtualizacaoFinaceiro.objects.last()

def povoar():
    inserir()
    RefereciaAtualizacaoFinaceiro.objects.create(referencia = mes_ano).save()

def verificar():
    if referencia.referencia != mes_ano:
        inserir()
        referencia.referencia = mes_ano
        referencia.save()
        definirGrupo(CasosCidade.objects.all())