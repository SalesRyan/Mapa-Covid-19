from sklearn.cluster import KMeans, AffinityPropagation, MeanShift, SpectralClustering, AgglomerativeClustering, DBSCAN, OPTICS, Birch
import pandas as pd


def agrupamento(df_nor, df_real, mode, n_groups = 3, verbose = 0):
    
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
 
    return final_groups, final_citys


# df_nor = pd.read_csv('final_normalizado 0 a 1.csv')
# df_real = pd.read_csv('final.csv')

# groups, citys = main(df_nor, df_real, 'kmeans', 3)

# print(groups)
# print(citys)