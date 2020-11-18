
def prepareJson(objeto,referencia):
    return {
        "nome": objeto['nome'],
        "obitos": objeto['obitos'],
        "confirmados": objeto['confirmados'],
        "incidencia": str(objeto['incidencia']).replace('.',','),
        "classeSom": objeto['classe'],
        "classe": int(objeto['incidencia']*10/(2*referencia)),
        "coordenadas": [{
            "lng":float(coordenadas.split(',')[0]),
            "lat":float(coordenadas.split(',')[1])
        }  for coordenadas in objeto['coordenadas'].split(' ')]
    }

def prepareRegioesJson(objeto,referencia_regioes):
    return {
        "nome": objeto['nome'],
        "obitos": objeto['obitos'],
        "confirmados": objeto['confirmados'],
        "incidencia": str(round(objeto['incidencia'],2)).replace('.',','),
        "classe": int(objeto['incidencia']*10/(2*referencia_regioes)),
        "coordenadas": [{
            "lng":float(coordenadas.split(',')[0]),
            "lat":float(coordenadas.split(',')[1])
        }  for coordenadas in objeto['coordenadas'].split(' ')]
    }

dicionario_color = {
    0: '#e85d04',
    1: '#dc2f02',
    2: '#9d0208',
    3: '#6a040f',
    4: '#370617',
    5: '#370617',
}

def data_min_max(dados):
    incidencia_min_max = list()
    for index in range(0,6):
        try:
            incidencia_min_max.append({
                'min':min(data['incidencia'] for data in dados if data['classe'] == index),
                'max':max(data['incidencia'] for data in dados if data['classe'] == index),
                'color':dicionario_color[index],
            })
        except :
            print(index)
    return incidencia_min_max