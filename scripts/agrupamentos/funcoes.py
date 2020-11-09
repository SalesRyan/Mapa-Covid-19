import time
import requests
from datetime import datetime, timedelta, date
from ast import literal_eval

def get_data_api(url, headers):
    response = requests.get(url, headers = headers)
    time.sleep(1)

    dados_dicio = literal_eval(response.text)

    dicio_zero = {
        'valor':0,
        'quantidadeBeneficiados':0,
    }

    if len(dados_dicio) == 0:
        dados_dicio = dicio_zero
    else:
        dados_dicio = dados_dicio[0]

    return dados_dicio

def get_last_year(data_atual,headers,nome,cod):
    mes_ano = None
    
    while mes_ano is None:
        ano = data_atual.year
        mes = data_atual.month
        if mes < 10:
            mes = '0' + str(mes)
        atual_mes_ano = str(ano) + str(mes)
        time.sleep(1)
        url = f'http://www.portaltransparencia.gov.br/api-de-dados/{nome}?mesAno={atual_mes_ano}&codigoIbge={cod}&pagina=1'

        r = requests.get(url, headers = headers)
        if r.text == '[]':
            data_atual = data_atual - timedelta(days = 31 )
        else:
            mes_ano = atual_mes_ano
    return mes_ano

def min_data(data_atual,headers_ae,headers_bf,headers_bpc,nomes,cod):
    mes_ano_list = list()
    mes_ano_list.append( get_last_year(data_atual,headers_ae,nomes[0],cod) )
    mes_ano_list.append( get_last_year(data_atual,headers_bf,nomes[1],cod) )
    mes_ano_list.append( get_last_year(data_atual,headers_bpc,nomes[2],cod) )
    return min(mes_ano_list)
    
    
