import pandas as pd
from dashboard.models import * 


nome = []
confirmados = []
obitos = []
incidencia = []
populacao = []

dados = list(CasosCidade.objects.all().values("nome","confirmados","obitos","incidencia","populacao" ))
for dados_dict in dados:
    nome.append(dados_dict['nome'])
    confirmados.append(dados_dict['confirmados'])
    obitos.append(dados_dict['obitos'])
    incidencia.append(dados_dict['incidencia'])
    populacao.append(dados_dict['populacao'])

dados_dict = {
    'nome':nome,
    'confirmados':confirmados,
    'obitos':obitos,
    'incidencia':incidencia,
    'populacao':populacao,
}

dados_dict = pd.DataFrame.from_dict(dados_dict)
dados_dict.to_csv("cidades.csv")

