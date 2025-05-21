# -*- coding: utf-8 -*-
"""
@author: nievesfo

Descripcion: Script para la aplicación del algoritmo no supervisado kmeans
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing, cluster
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
#%% FUNCIONES AUXILIARES

def plot_elbow(sse, ks):
    fig, axis = plt.subplots(figsize=(9, 6))
    axis.set_title('Método del codo para un k óptimo')
    axis.set_xlabel('k')
    axis.set_ylabel('SSE')
    plt.plot(ks, sse, marker='o')
    plt.tight_layout()
    plt.show()


def plot_silhouette(sils, ks):
    fig, axis = plt.subplots(figsize=(9, 6))
    axis.set_title('Método de la silueta')
    axis.set_xlabel('k')
    axis.set_ylabel('Silueta')
    plt.plot(ks, sils, marker='o')
    plt.tight_layout()
    plt.show()


def elbow_method(data):
    sse = []
    ks = range(2, 10)
    for k in ks:
        k_means_model = cluster.KMeans(n_clusters=k, random_state=55)
        k_means_model.fit(data)
        sse.append(k_means_model.inertia_)
    plot_elbow(sse, ks)


def silhouette_method(data):
    ks = range(2, 10)
    sils = []
    for k in ks:
        clusterer = KMeans(n_clusters=k, random_state=55)
        cluster_labels = clusterer.fit_predict(data)
        silhouette_avg = silhouette_score(data, cluster_labels)
        sils.append(silhouette_avg)
        print("Para n_clusters =", k, "El promedio de silhouette_score es:",
              silhouette_avg)
    plot_silhouette(sils, ks)

#%% CODIGO KMEANS    

if __name__ == '__main__':
    # Se carga el archivo de indicadores y se le hace una copia
    df = pd.read_csv("DATOS/CLEAN/general_data_v3.csv", sep=',', encoding='utf-8')
    dataset = df.copy()
    
    # Se crea una lista de todas las columnas de variables o features que se usarán 
    kpis = ['Inversion', 'Superficie (Ha.)','Población densidad (hab./Ha.)', 'Número Habitantes', 'Población Mujeres',
           'Edad media de la población', 'Personas con nacionalidad española','airbnb', 
           'poblacion_noEstudios','poblacion_estudios_medios', 'poblacion_estudios_superiores',
           'precio_vivienda','Personas con nacionalidad extranjera', 'Total hogares',"Tasa bruta de natalidad (‰)" ,
           "Población en etapas educativas", "Tasa de crecimiento demográfico (porcentaje)", 
           "Porcentaje de envejecimiento (Población mayor de 65 años/Población total)",
           "Tasa absoluta de paro registrado (febrero)", "Tamaño medio del hogar",  
           "Valor catastral medio por inmueble de uso residencial", "num_monoparental", 
           "Hogares con un hombre solo mayor de 65 años", 
           "Hogares con una mujer sola mayor de 65 años",
           "Renta neta media anual de los hogares (Urban Audit)"]
    
    # Se calculan las diferencias entre años
    for kpi in kpis:
        df[kpi] = np.where(df['anyo'] == 2020, -1 * df[kpi], df[kpi])
    
    # Se crea un nuevo dataframe 
    df = (df.groupby(['Barrio'])
            .agg(tasa_bruta_natalidad=('Tasa bruta de natalidad (‰)', sum), 
                 poblacion_etapa_educativa=('Población en etapas educativas', sum),
                 tasa_creci_demogr=('Tasa de crecimiento demográfico (porcentaje)', sum),
                 porcent_envejec=('Porcentaje de envejecimiento (Población mayor de 65 años/Población total)', sum),
                 paro_registrado=("Tasa absoluta de paro registrado (febrero)", sum),
                 tamanio_hogar=('Tamaño medio del hogar', sum),
                 valor_catastral_inmueble=('Valor catastral medio por inmueble de uso residencial', sum),
                 num_hogar_monoparental=('num_monoparental', sum),                
                 num_mujer_sola=('Hogares con una mujer sola mayor de 65 años', sum),
                 num_hombre_solo=('Hogares con un hombre solo mayor de 65 años', sum),
                 superficie=('Superficie (Ha.)', sum),
                 densidad=('Población densidad (hab./Ha.)', sum),
                 n_habitantes=('Número Habitantes', sum),
                 n_hab_mujeres=('Población Mujeres', sum),
                 edad_media_poblac=('Edad media de la población', sum),
                 num_espanioles=('Personas con nacionalidad española', sum),
                 airbnb=('airbnb', sum),
                 poblacion_noEstudios=('poblacion_noEstudios', sum),
                 poblacion_estudios_medios=('poblacion_estudios_medios', sum),
                 poblacion_estudios_superiores=('poblacion_estudios_superiores', sum),
                 precio_vivienda=('precio_vivienda', sum),
                 num_extranj=('Personas con nacionalidad extranjera', sum),
                 total_hogares=('Total hogares', sum),
                 inversion=('Inversion', sum),
                 renta=("Renta neta media anual de los hogares (Urban Audit)",sum)
                 )                
            .reset_index()
        )
    new_variable_names = ["tasa_bruta_natalidad","poblacion_etapa_educativa","tasa_creci_demogr", "porcent_envejec",
                         "paro_registrado", "tamanio_hogar", "valor_catastral_inmueble", "num_hogar_monoparental",
                         "renta", "num_mujer_sola", "num_hombre_solo",
                         "superficie", "densidad", "n_habitantes", "n_hab_mujeres", "edad_media_poblac","num_espanioles",
                         "airbnb", "poblacion_noEstudios", "poblacion_estudios_medios", "poblacion_estudios_superiores",
                         "precio_vivienda", "num_extranj", "total_hogares", "inversion"]
    for kpi in new_variable_names:
        df[kpi] = np.round(df[kpi], 2)
        
    #%% NORMALIZACION VARIABLES
    
    # Se crea una copia 
    df2 = df.copy()
    # Se elimina la columna Barrio para normalizar únicamente las variables numéricas
    df2 = df2.drop(columns=['Barrio'])
    x = df2.values
    # Se instancia el objeto para normalizar
    scaler = preprocessing.StandardScaler()
    x_scaled = scaler.fit_transform(x)
    # Se crea un Dataframe con cada una de las variables ya normalizadas
    df2 = pd.DataFrame(x_scaled)
    
    #%% CALCULO DE MATRIZ DE CORRELACIONES

    corr_matrix = df2.corr()
    corr_matrix = np.round(corr_matrix, 2)
    # Se representa en una figura
    fig, ax = plt.subplots(figsize=(15, 12))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='viridis', ax=ax, xticklabels=kpis, yticklabels=kpis)
    fig.show()
    
    #%% Se eliminan las filas altamente correlacionadas
    df2 = df2.drop(columns=[9,10,12,13,17,18,20,21,23])

    #%% APLICACION DEL METODO DE COMPONENTES PRINICPALES PARA REDUCIR EL NUMERO DE FEATURES
    # Se busca un número de componentes que aglutine el 90% de la varianza
    pca = PCA(0.9)
    pca.fit(df2)
    print(f'Variancia explicada PCA: {pca.explained_variance_ratio_}')
    print('Número de variables necesarias:', pca.n_components_)
    
    #Para representar los datos 
    plt.plot(pca.explained_variance_ratio_)
    plt.title("Algoritmo de componentes principales (PCA)")
    plt.ylabel('Varianza explicada')
    plt.xlabel('Componentes')
    plt.show()
    
    # Se crea un dataframe con las componentes principales
    columns = ['pca_comp_%i' % i for i in range(pca.n_components_)]
    df_pca  = pd.DataFrame(pca.transform(df2), columns=columns, index=df2.index)
    
    #%% ENCONTRAR K OPTIMO
    
    # Método de la silueta
    silhouette_method(df_pca)
    
    # Método del codo
    elbow_method(df_pca)
    # elbow 4 - silhouette 2 -> 3 -> 4
    
    #%% KMEANS K=3
    df_copy_k3 = df.copy()
    clusterer = KMeans(n_clusters=3, random_state=55)
    cluster_labels = clusterer.fit_predict(df_pca)
    df_copy_k3['cluster_k3'] = cluster_labels
    # Se relacionan los barrios con el cluster al que pertenece
    k3 = df_copy_k3[['Barrio', 'cluster_k3']]
    dataset_k3 = pd.merge(dataset, k3, on=['Barrio'])
    
    # Se agrupa por año y cluster, así se ve la tendencia por cada valor de k
    dataset_k3 = (
        dataset_k3
        .groupby(['anyo', 'cluster_k3'])
        .agg(tasa_bruta_natalidad=('Tasa bruta de natalidad (‰)', 'mean'), 
             poblacion_etapa_educativa=('Población en etapas educativas', 'mean'),
             tasa_creci_demogr=('Tasa de crecimiento demográfico (porcentaje)', 'mean'),
             porcent_envejec=('Porcentaje de envejecimiento (Población mayor de 65 años/Población total)', 'mean'),
             paro_registrado=('Tasa absoluta de paro registrado (febrero)', 'mean'),
             tamanio_hogar=('Tamaño medio del hogar', 'mean'),
             valor_catastral_inmueble=('Valor catastral medio por inmueble de uso residencial', 'mean'),
             num_hogar_monoparental=('num_monoparental', 'mean'),
             num_mujer_sola=('Hogares con una mujer sola mayor de 65 años', 'mean'),
             num_hombre_solo=('Hogares con un hombre solo mayor de 65 años', 'mean'),
             inversion=('Inversion', 'mean'),
             superficie=('Superficie (Ha.)', 'mean'),
             densidad=('Población densidad (hab./Ha.)', 'mean'),
             n_habitantes=('Número Habitantes', 'mean'),
             n_hab_mujeres=('Población Mujeres', 'mean'),
             edad_media_poblac=('Edad media de la población', 'mean'),
             num_espanioles=('Personas con nacionalidad española', 'mean'),
             airbnb=('airbnb', 'mean'),
             poblacion_noEstudios=('poblacion_noEstudios', 'mean'),
             poblacion_estudios_medios=('poblacion_estudios_medios', 'mean'),
             poblacion_estudios_superiores=('poblacion_estudios_superiores', 'mean'),
             precio_vivienda=('precio_vivienda', 'mean'),
             num_extranj=('Personas con nacionalidad extranjera', 'mean'),
             total_hogares=('Total hogares', 'mean'),
             renta=("Renta neta media anual de los hogares (Urban Audit)",'mean'))
        .reset_index()
    )
    dataset_k3.to_csv('DATOS/PREDICCION/dataset_clusters_3_flourish.csv', index=False)
    k3.to_csv('DATOS/PREDICCION/dataset_clusters_3_CARTO.csv', index=False)

    #%% KMEANS K=4
    df_copy_k4 = df.copy()
    clusterer = KMeans(n_clusters=4, random_state=55)
    cluster_labels = clusterer.fit_predict(df_pca)
    df_copy_k4['cluster_k4'] = cluster_labels
    # Se relacionan los barrios con el cluster al que pertenece
    k4 = df_copy_k4[['Barrio', 'cluster_k4']]
    dataset_k4 = pd.merge(dataset, k4, on=['Barrio'])
    
    # Se agrupa por año y cluster, así se ve la tendencia por cada valor de k
    dataset_k4 = (
        dataset_k4
        .groupby(['anyo', 'cluster_k4'])
        .agg(tasa_bruta_natalidad=('Tasa bruta de natalidad (‰)', 'mean'), 
             poblacion_etapa_educativa=('Población en etapas educativas', 'mean'),
             tasa_creci_demogr=('Tasa de crecimiento demográfico (porcentaje)', 'mean'),
             porcent_envejec=('Porcentaje de envejecimiento (Población mayor de 65 años/Población total)', 'mean'),
             paro_registrado=('Tasa absoluta de paro registrado (febrero)', 'mean'),
             tamanio_hogar=('Tamaño medio del hogar', 'mean'),
             valor_catastral_inmueble=('Valor catastral medio por inmueble de uso residencial', 'mean'),
             num_hogar_monoparental=('num_monoparental', 'mean'),
             num_mujer_sola=('Hogares con una mujer sola mayor de 65 años', 'mean'),
             num_hombre_solo=('Hogares con un hombre solo mayor de 65 años', 'mean'),
             inversion=('Inversion', 'mean'),
             superficie=('Superficie (Ha.)', 'mean'),
             densidad=('Población densidad (hab./Ha.)', 'mean'),
             n_habitantes=('Número Habitantes', 'mean'),
             n_hab_mujeres=('Población Mujeres', 'mean'),
             edad_media_poblac=('Edad media de la población', 'mean'),
             num_espanioles=('Personas con nacionalidad española', 'mean'),
             airbnb=('airbnb', 'mean'),
             poblacion_noEstudios=('poblacion_noEstudios', 'mean'),
             poblacion_estudios_medios=('poblacion_estudios_medios', 'mean'),
             poblacion_estudios_superiores=('poblacion_estudios_superiores', 'mean'),
             precio_vivienda=('precio_vivienda', 'mean'),
             num_extranj=('Personas con nacionalidad extranjera', 'mean'),
             total_hogares=('Total hogares', 'mean'),
             renta=("Renta neta media anual de los hogares (Urban Audit)",'mean'))
        .reset_index()
    )
    dataset_k4.to_csv('DATOS/PREDICCION/dataset_clusters_4_flourish.csv', index=False)
    k4.to_csv('DATOS/PREDICCION/dataset_clusters_4_CARTO.csv', index=False)



