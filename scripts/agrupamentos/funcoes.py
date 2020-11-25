import time
import requests
from datetime import datetime, timedelta, date
from ast import literal_eval

def get_data_api(url, headers):
    while True:
        try:    
            response = requests.get(url, headers = headers)
            time.sleep(3)

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
        except:
            time.sleep(3)
            print('Exception em get_data_api, tentando novamente')
            continue

def get_last_year(data_atual,headers,nome,cod):
    mes_ano = None
    while True:
        try:
            while mes_ano is None:
                ano = data_atual.year
                mes = data_atual.month
                if mes < 10:
                    mes = '0' + str(mes)
                atual_mes_ano = str(ano) + str(mes)
                time.sleep(3)
                url = f'http://www.portaltransparencia.gov.br/api-de-dados/{nome}?mesAno={atual_mes_ano}&codigoIbge={cod}&pagina=1'

                r = requests.get(url, headers = headers)
                if r.text == '[]':
                    data_atual = data_atual - timedelta(days = 31 )
                else:
                    mes_ano = atual_mes_ano
            return mes_ano
        except:
            time.sleep(3)
            print('Exception em get_last_year')
            continue


def min_data(data_atual,headers,nomes,cod):
    mes_ano_list = list()
    mes_ano_list.append(get_last_year(data_atual,headers,nomes[0],cod))
    mes_ano_list.append(get_last_year(data_atual,headers,nomes[1],cod))
    mes_ano_list.append(get_last_year(data_atual,headers,nomes[2],cod))
    return min(mes_ano_list)
    
    
