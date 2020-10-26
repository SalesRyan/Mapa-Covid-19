
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