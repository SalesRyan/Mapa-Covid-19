from sklearn.cluster import KMeans, AffinityPropagation, MeanShift, SpectralClustering, AgglomerativeClustering, DBSCAN, OPTICS, Birch
import pandas as pd

from dashboard.models import *
from unidecode import unidecode



def agrupamento(df_nor=pd.read_csv('scripts/agrupamentos/df_normalizado.csv'), df_real=pd.read_csv('scripts/agrupamentos/df_normal.csv'), mode='kmeans', n_groups = 3, verbose = 0):
    
    if verbose:
        print('Show DataFrames:')
        print('- DataFrames Normalization')
        print(df_nor.tail(5))    
        print('- DataFrames Real')
        print(df_real.tail(5))
    
    
    X = df_nor.drop(['MUNICIPIO', 'QTD_BPC', 'VALOR_BPC'],axis=1).values
    y = df_nor['MUNICIPIO'].values
    
    pred = []
    
    if mode == 'kmeans':
        
        kmeans = KMeans(n_clusters=n_groups, random_state=0).fit(X)
        pred =  kmeans.labels_
    
    elif mode == 'AffinityPropagation':
        
        affinity = AffinityPropagation().fit(X)
        pred =  affinity.labels_
    
    elif mode == 'MeanShift':
    
        mean_shift = MeanShift(bandwidth=9).fit(X)
        pred =  mean_shift.labels_
    
    elif mode == 'SpectralClustering':
        
        spectral_clustering = SpectralClustering(n_clusters=n_groups, assign_labels="discretize", random_state=0).fit(X)
        pred =  spectral_clustering.labels_
    
    elif mode == 'AgglomerativeClustering':
        
        agglomerative_clustering = AgglomerativeClustering().fit(X)
        pred =  agglomerative_clustering.labels_
    
    elif mode == 'DBSCAN':
        
        dbscan = DBSCAN(eps=3, min_samples=2).fit(X)
        pred =  dbscan.labels_
    
    elif mode == 'OPTICS':
        
        optics = OPTICS(min_samples=2).fit(X)
        pred =  optics.labels_
    
    elif mode == 'Birch':
        
        brc = Birch(n_clusters=None).fit(X)
        pred =  brc.labels_
    
    
    result = [[] for i in range(pred.max()+1)]
    
    for group, label in zip(pred,y):

        result[group].extend([label])
    

    df_real = df_real.set_index('MUNICIPIO')
    
    final_groups = []
    final_citys =  []
    
    for index,var in enumerate([pd.DataFrame()]*len(result)):
        
        var = df_real.loc[result[index]]
        
        final_groups.append(var)
        final_citys.append(result[index])
        
        if verbose:
            print('--------------------------')
            print('\nGrupo',index,'\n')

            print(var.describe())
            print(result[index])
 
    return final_citys


# df_nor = pd.read_csv('final_normalizado 0 a 1.csv')
# df_real = pd.read_csv('final.csv')

# groups, citys = main(df_nor, df_real, 'kmeans', 3)

# print(groups)
# print(citys)

def classAgrupamento(nome):
    objs = DadosFinanceiros.objects.all()
    dicio = {
        'MUNICIPIO':[],
        'VALOR_BF':[],
        'QTD_BF':[],
        'VALOR_AE':[],
        'QTD_AE':[],
        'VALOR_BPC':[],
        'QTD_BPC':[],
        'CONF':[],
        'OBT':[],
        'INC':[],
        'POP':[]
    }
    for obj in objs:
        dicio['MUNICIPIO'].append(obj.cidade.nome)
        dicio['VALOR_BF'].append(obj.valor_bolsa_familia)
        dicio['QTD_BF'].append(obj.quantidade_bolsa_familia)
        dicio['VALOR_AE'].append(obj.valor_auxilio_emergencial)
        dicio['QTD_AE'].append(obj.quantidade_auxilio_emergencial)
        dicio['VALOR_BPC'].append(obj.valor_BPC)
        dicio['QTD_BPC'].append(obj.quantidade_BPC)
        dicio['CONF'].append(obj.cidade.confirmados)
        dicio['OBT'].append(obj.cidade.obitos)
        dicio['INC'].append(obj.cidade.incidencia)
        dicio['POP'].append(obj.cidade.populacao)
    df = pd.DataFrame(dicio)
    df_normalizado = df.apply(lambda x: pd.Series([x[0], x[1]/x[10], x[2]/x[10], x[3]/x[10], x[4]/x[10], x[5]/x[10], x[6]/x[10], x[7]/x[10], x[8]/x[10], x[9]]), axis=1 ,raw=True)
    df_normalizado = df_normalizado.rename(columns={x:y for x,y in enumerate(dicio.keys())})
    grupos = agrupamento(df_real=df, df_nor=df_normalizado) 
    grupos = [[cidade.replace("'","") for cidade in grupo] for grupo in grupos]
    for index,grupo in enumerate(grupos):
        if unidecode(nome) in grupo:
            return index
    return -1

def definirGrupo(objs):
    print('Definindo grupos do agrupamento casosCidade agrupamento')
    for obj in objs:
        obj.classe=classAgrupamento(obj.nome)
        obj.save() 