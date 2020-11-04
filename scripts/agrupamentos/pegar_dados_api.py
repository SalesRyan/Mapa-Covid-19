import pandas as pd
import numpy as np

import requests
import time
from datetime import datetime, timedelta, date

from ast import literal_eval
import json
import pandas as pd
import numpy as np

df = pd.read_excel('arquivos_auxiliares/Extração de dados/cidades.xlsx')
codigos = df['Codigo'].to_list()

headers = {'Accept': 'application/json', 'chave-api-dados': '97ffcd5175f477ecee3cf0513575369a'}

cod_teresina = '2211001'
data_atual = date.today()
mes_ano = None
while mes_ano is None:
    ano = data_atual.year
    mes = data_atual.month
    if mes < 10:
        mes = '0' + str(mes)
    atual_mes_ano = str(ano) + str(mes)
    url = f'http://www.portaltransparencia.gov.br/api-de-dados/auxilio-emergencial-por-municipio?mesAno={atual_mes_ano}&codigoIbge={cod_teresina}&pagina=1'
    r = requests.get(url, headers = headers)
    if r.text == '[]':
        data_atual = data_atual - timedelta(days = 31 )
    else:
        mes_ano = atual_mes_ano

nomes = ['bpc-por-municipio', 'bolsa-familia-por-municipio', 'auxilio-emergencial-por-municipio']
headers_ae = {'Accept': 'application/json', 'chave-api-dados': '97ffcd5175f477ecee3cf0513575369a'}
headers_bf = {'Accept': 'application/json', 'chave-api-dados': 'cd3ce70479a54938a00eb513f67264ad'}
headers_bpc = {'Accept': 'application/json', 'chave-api-dados': 'd9d68d738cd1263bbbdfb653c848826b'}

for cod in codigos:
    url = f'http://www.portaltransparencia.gov.br/api-de-dados/{nomes[0]}?mesAno={mes_ano}&codigoIbge={cod}&pagina=1'
    url = f'http://www.portaltransparencia.gov.br/api-de-dados/{nomes[1]}?mesAno={mes_ano}&codigoIbge={cod}&pagina=1'
    url = f'http://www.portaltransparencia.gov.br/api-de-dados/{nomes[2]}?mesAno={mes_ano}&codigoIbge={cod}&pagina=1'
    
    response_ae = requests.get(url, headers = headers_ae)
    response_bf = requests.get(url, headers = headers_bf)
    response_bpc = requests.get(url, headers = headers_bpc)

    dados_dicio_bf = literal_eval(response_bf.text)[0]
    dados_dicio_ae = literal_eval(response_ae.text)[0]
    dados_dicio_bpc = literal_eval(response_bpc.text)[0]
    
    cidade = CasosCidade.objects.get(name=dados_dicio['nomeIBGEsemAcento'])
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

