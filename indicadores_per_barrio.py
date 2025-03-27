# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 11:37:58 2025

@author: Nievesita
"""

import pandas as pd
import numpy as np
import os
import utm
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from ast import literal_eval
import xml.etree.ElementTree as ET
from geopy.geocoders import Photon
import clean_and_select_places
import xlrd
import openpyxl

#%%

def cambia_nombre_lista(list_categoria):
    rep_map = {'Población densidad (hab./Ha.)':'Densidad (hab./Ha.)',
               'Sexo de la población':'Número Habitantes',
               'Mujeres':'Población Mujeres',
               'Nº total de hogares':'Total hogares',
               'Paro registrado (nº de personas registradas en SEPE en febrero 2020)':'Paro registrado (número de personas registradas en SEPE en febrero)',
               'Nº Total de viviendas familiares (Censo Edificios y Viviendas 2011)':'Número de inmuebles de uso residencial',
               'Superficie media de la vivienda (m2) en transacción (2019)':'Superficie media de la vivienda (m2) en transacción',
               'Nº de Bibliotecas Municipales':'Bibliotecas públicas Municipales',
               'Nº de Bibliotecas Comunidad Madrid':'Bibliotecas públicas Comunidad Madrid',
               'Nº de Centros Culturales':'Centros y Espacios Culturales',
               'Nº de Centros y Espacios Culturales':'Centros y Espacios Culturales',
               'Personas con nacionalidad española (01/01/2020)':'Personas con nacionalidad española',
               'Personas con nacionalidad extranjera (01/01/2020)':'Personas con nacionalidad extranjera',
               'Paro registrado (nº de personas registradas en SEPE en febrero 2021)':'Paro registrado (número de personas registradas en SEPE en febrero)',
               'Número de inmuebles de uso residencial (2019)':'Número de inmuebles de uso residencial',
               ' (01/01/2021)':'',
               'Personas con nacionalidad española (01/01/2021)':'Personas con nacionalidad española',
               'Personas con nacionalidad extranjera (01/01/2021)':'Personas con nacionalidad extranjera',
               'Paro registrado (nº de personas registradas en SEPE en febrero 2022)':'Paro registrado (número de personas registradas en SEPE en febrero)',
               'Número de inmuebles de uso residencial (2020)': 'Número de inmuebles de uso residencial',
               'Superficie media de la vivienda (m2) en transacción (2020)':'Superficie media de la vivienda (m2) en transacción',
               ' (01/01/2022)':' ',
               'Paro registrado (nº de personas registradas en SEPE en febrero 2023)':'Paro registrado (nº de personas registradas en SEPE en febrero)',
               'Mercados Municipales (2022)':'Mercados Municipales',
               'Personas con nacionalidad española (01/01/2022)':'Personas con nacionalidad española',
               'Personas con nacionalidad extranjera (01/01/2022)':'Personas con nacionalidad extranjera'
               }
    #list_categoria = [w.replace('Densidad (hab./Ha.)', 'Población densidad (hab./Ha.)') for w in list_categoria]
    list_categoria = [rep_map.get(word, word) for word in list_categoria]
    return list_categoria

def extract_indicators():
    

    index_elimina_nan = ["Superficie (Ha.)", "Población densidad (hab./Ha.)","Densidad (hab./Ha.)", "Edad media de la población", 
                          "Tamaño medio del hogar","Centros Municipales de Mayores","Centros de Servicios Sociales", 
                          "Centros de Día de Alzheimer y Físicos", "Residencias para personas Mayores", "Centros para personas sin hogar",
                          "Espacios de Igualdad", "Centros de Atención a las Adicciones (CAD y CCAD)", "Bibliotecas públicas Municipales",
                          "Nº de Bibliotecas Municipales", "Nº de Bibliotecas Comunidad Madrid","Nº de Centros Culturales",
                          "Bibliotecas públicas Comunidad Madrid", "Centros y Espacios Culturales",
                          "Centros Municipales de Salud Comunitaria (CMSC)"]
    index_guardar_impares = ["Número Habitantes","Sexo de la población", "Población Mujeres","Mujeres", "Personas con nacionalidad española", 
                              "Personas con nacionalidad extranjera", "Total hogares", "Nº total de hogares",
                              "Nº Total de viviendas familiares (Censo Edificios y Viviendas 2011)","Mercados Municipales",
                              "Paro registrado (número de personas registradas en SEPE en febrero)", 
                              "Paro registrado (nº de personas registradas en SEPE en febrero 2020)", 
                              "Número de inmuebles de uso residencial","Nº Total de viviendas (Censo Edificios y Viviendas 2011)",
                              "Superficie media construida (m2) inmuebles de uso residencial",
                              "Superficie media de la vivienda (m2) en transacción (2019)" ]

    index_sum_centro_social = ["Centros de Servicios Sociales", "Centros Municipales de Mayores","Centros para personas sin hogar",
                                "Espacios de Igualdad", "Centros de Atención a las Adicciones (CAD y CCAD)"]
    index_sum_bibliotecas_y_cultural = ["Bibliotecas públicas Municipales","Bibliotecas públicas Comunidad Madrid", 
                                         "Centros y Espacios Culturales"]

    index_escuela_infantil_primaria = ["Escuelas Infantiles Municipales","Colegios Públicos Infantil y Primaria"]
     
    distritos = ['CENTRO', 'ARGANZUELA', 'RETIRO', 'SALAMANCA', 'CHAMARTÍN', 'TETUÁN', 'CHAMBERÍ', 'FUENCARRAL-EL PARDO', 
                  'MONCLOA-ARAVACA', 'LATINA', 'CARABANCHEL', 'USERA', 'PUENTE DE VALLECAS', 'MORATALAZ', 'CIUDAD LINEAL', 
                  'HORTALEZA', 'VILLAVERDE', 'VILLA DE VALLECAS', 'VICÁLVARO', 'SAN BLAS-CANILLEJAS', 'BARAJAS']
    rows_2020 = [0,2,3,6,8,9,25,28,35,252,255,311,312,313,315,321,323,325,326,328,329,330,354]
    rows_2021 = [0,2,3,6,8,9,25,28,35,268,273,327,328,329,331,337,339,341,342,344,345,346,370]
    rows_2022 = [0,2,3,6,8,9,25,28,35,256,261,315,316,317,319,325,327,329,330,332,333,334,357]
    rows_2023 = [0,2,3,6,8,9,24,27,34,246,251,306,307,308,310,316,318,320,321,323,324,325,348]
    rows_2024 = [0,2,3,6,8,9,24,27,34,230,234,289,290,291,293,299,301,303,304,306,307,308,331]
    rows_ = {2020:rows_2020, 2021:rows_2021,2022:rows_2022,2023:rows_2023,2024:rows_2024}
    path = "DATOS/renta/INDICADORES"
    anyo = list(range(2020,2025))
    categorias = ["Barrio","anyo","Distrito"]
    df_final_distritos = pd.DataFrame() 
    df_final_anyo = pd.DataFrame() 
    dir_list = os.listdir(path)
    for file_name in range(len(dir_list)):
        print("Reading ", dir_list[file_name])  
        df = pd.read_excel(str(path)+"/"+str(dir_list[file_name]),sheet_name=None, decimal=',',header=0)
        df_final_barrios = pd.DataFrame() 
             
        for district in distritos:
            #print("Distrito ", district)
            distrito_sheet_df  = df[district].iloc[rows_[anyo[file_name]], :]
            #df_indicadores = df.iloc[rows, :]
            #print(distrito_sheet_df.columns[1])
            categorias = ["Barrio","anyo","Distrito"]
            #categorias = list(df_indicadores[df_indicadores.columns[1]])
            if anyo[file_name] == 2020 or anyo[file_name] == 2021 or anyo[file_name] == 2022:
                categorias.extend(cambia_nombre_lista(list(distrito_sheet_df[distrito_sheet_df.columns[0]])))
                
                barrios = list(distrito_sheet_df.iloc[0,5:].dropna())
            else:
                categorias.extend(cambia_nombre_lista(list(distrito_sheet_df[distrito_sheet_df.columns[1]])))
                barrios = list(distrito_sheet_df.iloc[0,6:].dropna())
            
            categorias = list(filter(str.strip, categorias))
            categorias = list(map(str.strip, categorias))
            #barrios = list(distrito_sheet_df.iloc[0,6:18].dropna())
            df_transpose = distrito_sheet_df.T
             
            dict_indicadores = {}
            for row in range(1,len(distrito_sheet_df)):
                    #print( row, " "+categorias[row+2])
                    if anyo[file_name] == 2020 or anyo[file_name] == 2021 or anyo[file_name] == 2022:
                        df_aux =  distrito_sheet_df.iloc[row,5:]
                        
                    else:
                        df_aux =  distrito_sheet_df.iloc[row,6:]
                    #dict_indicadores[categorias[row+2]] = list(df_aux)
                    if (categorias[row+2].strip() in index_elimina_nan) or (len(list(df_aux.dropna())) == len(barrios)):
                        aux_list = list(df_aux.dropna())
                        if len(aux_list) >  len(barrios):
                            delete_item = -(len(aux_list) - len(barrios))
                            aux_list = aux_list[:delete_item]
                        dict_indicadores[categorias[row+2]] = aux_list
                    if (categorias[row+2].strip() in index_guardar_impares) and (len(list(df_aux.dropna())[1::2])== len(barrios)) :
                        aux_list = list(df_aux.dropna())[1::2]
                        if len(aux_list) >  len(barrios):
                            delete_item = -(len(aux_list) - len(barrios))
                            aux_list = aux_list[:delete_item]
                        dict_indicadores[categorias[row+2]] = aux_list
            dict_indicadores["Barrio"] = barrios
            dict_indicadores["anyo"] =  np.repeat(anyo[file_name],len(barrios))
            df_final_barrios = pd.concat([df_final_barrios, pd.DataFrame.from_dict(dict_indicadores)], ignore_index=True, sort=False)
        df_final_distritos =  pd.concat([df_final_distritos, df_final_barrios], ignore_index=True, sort=False)
    df_final_anyo = pd.concat([df_final_anyo, df_final_distritos], ignore_index=True, sort=False)

    # Se termina de solucionar el problema que estas dos colmunas
    fix_density_col = list(df_final_anyo["Densidad (hab./Ha.)"].dropna())+list(df_final_anyo["Población densidad (hab./Ha.)"].dropna())
    df_final_anyo["Densidad (hab./Ha.)"] = fix_density_col

    # Se borran finalmente las columnas sin informacion y duplicadas
    df_final_anyo = df_final_anyo.drop(columns=["Población densidad (hab./Ha.)","Superficie media de la vivienda (m2) en transacción"])

    # Se ordena el dataframe segun el año y el barrio
    df_final_anyo.sort_values(by=['Barrio', 'anyo'], ascending=[True, True], inplace=True)
    return df_final_anyo

def merge_dataframes_with_main(df_to_merge_with_main):
    df_general = pd.read_csv("DATOS/CLEAN/general_data.csv", sep=',', encoding='utf-8')
    dfinal = df_general.merge(df_to_merge_with_main, left_on=['Barrio', 'anyo'], right_on=['Barrio', 'anyo'])
    return dfinal
    
        
        
         
    


    
#%%
if __name__ == '__main__':
    df_indicadores_poblacion = extract_indicators()
    df_merge = merge_dataframes_with_main(df_indicadores_poblacion)
    print("Creating general_data csv...")
    clean_and_select_places.create_csv(df_merge, 'DATOS/CLEAN/', "general_data.csv")
    print("main")
    


#%%
index_elimina_nan = ["Superficie (Ha.)", "Población densidad (hab./Ha.)", "Edad media de la población", 
                     "Tamaño medio del hogar", "Tasa bruta de natalidad (‰)", "Tasa de crecimiento demográfico (porcentaje)",
                     "Índice de Vulnerabilidad Bienestar Social e Igualdad", "Índice de Vulnerabilidad Medio Ambiente Urbano y Movilidad",
                     "Índice de Vulnerabilidad Educación y Cultura", "Índice de Vulnerabilidad Economía y Empleo",
                     "Índice de Vulnerabilidad Salud", "Centros de Servicios Sociales", "Centros Municipales de Mayores",
                     "Centros de Día de Alzheimer y Físicos", "Residencias para personas Mayores", "Centros para personas sin hogar",
                     "Espacios de Igualdad", "Centros de Atención a las Adicciones (CAD y CCAD)", "Bibliotecas públicas Municipales",
                     "Bibliotecas públicas Comunidad Madrid", "Centros y Espacios Culturales","Instalaciones deportivas básicas",
                     "Centros deportivos municipales", "Escuelas Infantiles Municipales","Colegios Públicos Infantil y Primaria"]
index_guardar_impares = ["Número Habitantes", "Población Mujeres", "Personas con nacionalidad española", 
                         "Personas con nacionalidad extranjera", "Total hogares", 
                         "Paro registrado (número de personas registradas en SEPE en febrero)", 
                         "Número de inmuebles de uso residencial", "Superficie media construida (m2) inmuebles de uso residencial",
                         "Mercados Municipales", "Asociaciones (Sección 1ª)", "Asociaciones culturales y casas regionales",
                         "Asociaciones de mujeres", "Asociaciones vecinales", "Fundaciones (Sección 2ª)"]

rows_2020 = [0,2,3,6,8,9,25,28,35,36,42,43,66,243,252,311,312,313,315,321,323,325,326,328,329,330,332,334,354,357,358,359,360,361]
rows_2021 = [0,2,3,6,8,9,25,28,35,36,42,43,66,268,273,327,328,329,331,337,339,341,342,344,345,346,348,350,370,373,374,375,376,377]
rows_2022 = [0,2,3,6,8,9,25,28,35,36,42,43,66,256,261,315,316,317,319,325,327,329,330,332,333,334,336,337,357,360,361,362,363,364]
rows_2023 = [0,2,3,6,8,9,24,27,30,34,35,41,42,64,246,251,306,307,308,310,316,318,320,321,323,324,325,327,328,348,356,357,358,359,360]
rows_2024 = [0,2,3,6,8,9,24,27,30,34,35,41,42,62,230,234,289,290,291,293,299,301,303,304,306,307,308,310,311,331,339,340,341,342,343]
path = "DATOS/renta/INDICADORES"

#print("Reading ", dir_list[file_name])  
df = pd.read_excel(str(path)+"/panel_indicadores_distritos_barrios_2024.xlsx",sheet_name=None, decimal=',',header=0)
df_final_barrios = pd.DataFrame() 
         
for district in distritos:
    print("distrito ", district)
    distrito_sheet_df  = df[district].iloc[rows_[anyo[file_name]], :]
        #df_indicadores = df.iloc[rows, :]
        #print(distrito_sheet_df.columns[1])
    categorias = ["Barrio","anyo","Distrito"]
        #categorias = list(df_indicadores[df_indicadores.columns[1]])
    if anyo[file_name] == 2020 or anyo[file_name] == 2021 or anyo[file_name] == 2022:
         categorias.extend(cambia_nombre_lista(list(distrito_sheet_df[distrito_sheet_df.columns[0]])))
         barrios = list(distrito_sheet_df.iloc[0,5:].dropna())
    else:
            #print("entra en el else")
         categorias.extend(cambia_nombre_lista(list(distrito_sheet_df[distrito_sheet_df.columns[1]])))
         barrios = list(distrito_sheet_df.iloc[0,6:].dropna())
        
    categorias = list(map(str.strip, categorias))
        #print(categorias)
        #barrios = list(distrito_sheet_df.iloc[0,6:18].dropna())
    df_transpose = distrito_sheet_df.T
         
    dict_indicadores = {}
    for row in range(1,len(distrito_sheet_df)):
              #print( row, " "+categorias[row+2])
        if anyo[file_name] == 2020 or anyo[file_name] == 2021 or anyo[file_name] == 2022:
            df_aux =  distrito_sheet_df.iloc[row,5:]
        else:
            df_aux =  distrito_sheet_df.iloc[row,6:]
                #print(list(df_aux)) 
                #dict_indicadores[categorias[row+2]] = list(df_aux)
            if (categorias[row+2].strip() in index_elimina_nan) or (len(list(df_aux.dropna())) == len(barrios)):
                aux_list = list(df_aux.dropna())
                if len(aux_list) >  len(barrios):
                    delete_item = -(len(aux_list) - len(barrios))
                    aux_list = aux_list[:delete_item]
                dict_indicadores[categorias[row+2]] = aux_list
                    #print("ntra")
            if (categorias[row+2].strip() in index_guardar_impares) and (len(list(df_aux.dropna())[1::2])== len(barrios)) :
                aux_list = list(df_aux.dropna())[1::2]
                if len(aux_list) >  len(barrios):
                    delete_item = -(len(aux_list) - len(barrios))
                    aux_list = aux_list[:delete_item]
                dict_indicadores[categorias[row+2]] = aux_list
                    #print("segundo if ", list(df_aux.dropna())[1::2])
            dict_indicadores["Barrio"] = barrios
        dict_indicadores["Anyo"] =  np.repeat(anyo[file_name],len(barrios))
        #df_final_barrios = pd.DataFrame.from_dict(dict_indicadores)
        df_final_barrios = pd.concat([df_final_barrios, pd.DataFrame.from_dict(dict_indicadores)], ignore_index=True, sort=False)
    df_final_distritos =  pd.concat([df_final_distritos, df_final_barrios], ignore_index=True, sort=False)
df_final_anyo = pd.concat([df_final_anyo, df_final_distritos], ignore_index=True, sort=False)
    
    
#%%
#df0 = pd.read_excel(str(path)+"/panel_indicadores_distritos_barrios_2020.xls",sheet_name="ARGANZUELA", decimal=',',header=0)
df1 = pd.read_excel(str(path)+"/panel_indicadores_distritos_barrios_2021.xlsx",sheet_name="ARGANZUELA", decimal=',',header=0)
df2 = pd.read_excel(str(path)+"/panel_indicadores_distritos_barrios_2022.xlsx",sheet_name="ARGANZUELA", decimal=',',header=0)
df3 = pd.read_excel(str(path)+"/panel_indicadores_distritos_barrios_2023.xlsx",sheet_name="ARGANZUELA", decimal=',',header=0)
#df4 = pd.read_excel(str(path)+"/panel_indicadores_distritos_barrios_2024.xlsx",sheet_name="ARGANZUELA", decimal=',',header=0)



#%%
def cambia_nombre_lista(list_categoria):
    rep_map = {'Población densidad (hab./Ha.)':'Densidad (hab./Ha.)',
               'Sexo de la población':'Número Habitantes',
               'Mujeres':'Población Mujeres',
               'Nº total de hogares':'Total hogares',
               'Paro registrado (nº de personas registradas en SEPE en febrero 2020)':'Paro registrado (número de personas registradas en SEPE en febrero)',
               'Nº Total de viviendas familiares (Censo Edificios y Viviendas 2011)':'Número de inmuebles de uso residencial',
               'Superficie media de la vivienda (m2) en transacción (2019)':'Superficie media de la vivienda (m2) en transacción',
               'Nº de Bibliotecas Municipales':'Bibliotecas públicas Municipales',
               'Nº de Bibliotecas Comunidad Madrid':'Bibliotecas públicas Comunidad Madrid',
               'Nº de Centros Culturales':'Centros y Espacios Culturales',
               'Nº de Centros y Espacios Culturales':'Centros y Espacios Culturales',
               'Personas con nacionalidad española (01/01/2020)':'Personas con nacionalidad española',
               'Personas con nacionalidad extranjera (01/01/2020)':'Personas con nacionalidad extranjera',
               'Paro registrado (nº de personas registradas en SEPE en febrero 2021)':'Paro registrado (número de personas registradas en SEPE en febrero)',
               'Número de inmuebles de uso residencial (2019)':'Número de inmuebles de uso residencial',
               ' (01/01/2021)':'',
               'Personas con nacionalidad española (01/01/2021)':'Personas con nacionalidad española',
               'Personas con nacionalidad extranjera (01/01/2021)':'Personas con nacionalidad extranjera',
               'Paro registrado (nº de personas registradas en SEPE en febrero 2022)':'Paro registrado (número de personas registradas en SEPE en febrero)',
               'Número de inmuebles de uso residencial (2020)': 'Número de inmuebles de uso residencial',
               'Superficie media de la vivienda (m2) en transacción (2020)':'Superficie media de la vivienda (m2) en transacción',
               ' (01/01/2022)':' ',
               'Paro registrado (nº de personas registradas en SEPE en febrero 2023)':'Paro registrado (nº de personas registradas en SEPE en febrero)',
               'Mercados Municipales (2022)':'Mercados Municipales',
               'Personas con nacionalidad española (01/01/2022)':'Personas con nacionalidad española',
               'Personas con nacionalidad extranjera (01/01/2022)':'Personas con nacionalidad extranjera'
               }
    #list_categoria = [w.replace('Densidad (hab./Ha.)', 'Población densidad (hab./Ha.)') for w in list_categoria]
    list_categoria = [rep_map.get(word, word) for word in list_categoria]
    return list_categoria

index_elimina_nan = ["Superficie (Ha.)", "Población densidad (hab./Ha.)","Densidad (hab./Ha.)", "Edad media de la población", 
                      "Tamaño medio del hogar","Centros Municipales de Mayores","Centros de Servicios Sociales", 
                      "Centros de Día de Alzheimer y Físicos", "Residencias para personas Mayores", "Centros para personas sin hogar",
                      "Espacios de Igualdad", "Centros de Atención a las Adicciones (CAD y CCAD)", "Bibliotecas públicas Municipales",
                      "Nº de Bibliotecas Municipales", "Nº de Bibliotecas Comunidad Madrid","Nº de Centros Culturales",
                      "Bibliotecas públicas Comunidad Madrid", "Centros y Espacios Culturales",
                      "Centros Municipales de Salud Comunitaria (CMSC)"]
index_guardar_impares = ["Número Habitantes","Sexo de la población", "Población Mujeres","Mujeres", "Personas con nacionalidad española", 
                          "Personas con nacionalidad extranjera", "Total hogares", "Nº total de hogares",
                          "Nº Total de viviendas familiares (Censo Edificios y Viviendas 2011)","Mercados Municipales",
                          "Paro registrado (número de personas registradas en SEPE en febrero)", 
                          "Paro registrado (nº de personas registradas en SEPE en febrero 2020)", 
                          "Número de inmuebles de uso residencial","Nº Total de viviendas (Censo Edificios y Viviendas 2011)",
                          "Superficie media construida (m2) inmuebles de uso residencial",
                          "Superficie media de la vivienda (m2) en transacción (2019)" ]

index_sum_centro_social = ["Centros de Servicios Sociales", "Centros Municipales de Mayores","Centros para personas sin hogar",
                            "Espacios de Igualdad", "Centros de Atención a las Adicciones (CAD y CCAD)"]
index_sum_bibliotecas_y_cultural = ["Bibliotecas públicas Municipales","Bibliotecas públicas Comunidad Madrid", 
                                     "Centros y Espacios Culturales"]

index_escuela_infantil_primaria = ["Escuelas Infantiles Municipales","Colegios Públicos Infantil y Primaria"]
 
distritos = ['CENTRO', 'ARGANZUELA', 'RETIRO', 'SALAMANCA', 'CHAMARTÍN', 'TETUÁN', 'CHAMBERÍ', 'FUENCARRAL-EL PARDO', 
              'MONCLOA-ARAVACA', 'LATINA', 'CARABANCHEL', 'USERA', 'PUENTE DE VALLECAS', 'MORATALAZ', 'CIUDAD LINEAL', 
              'HORTALEZA', 'VILLAVERDE', 'VILLA DE VALLECAS', 'VICÁLVARO', 'SAN BLAS-CANILLEJAS', 'BARAJAS']
rows_2020 = [0,2,3,6,8,9,25,28,35,252,255,311,312,313,315,321,323,325,326,328,329,330,354]
rows_2021 = [0,2,3,6,8,9,25,28,35,268,273,327,328,329,331,337,339,341,342,344,345,346,370]
rows_2022 = [0,2,3,6,8,9,25,28,35,256,261,315,316,317,319,325,327,329,330,332,333,334,357]
rows_2023 = [0,2,3,6,8,9,24,27,34,246,251,306,307,308,310,316,318,320,321,323,324,325,348]
rows_2024 = [0,2,3,6,8,9,24,27,34,230,234,289,290,291,293,299,301,303,304,306,307,308,331]
rows_ = {2020:rows_2020, 2021:rows_2021,2022:rows_2022,2023:rows_2023,2024:rows_2024}
path = "DATOS/renta/INDICADORES"
anyo = list(range(2020,2025))
categorias = ["Barrio","anyo","Distrito"]
df_final_distritos = pd.DataFrame() 
df_final_anyo = pd.DataFrame() 
dir_list = os.listdir(path)
for file_name in range(len(dir_list)):
    print("Reading ", dir_list[file_name])  
    df = pd.read_excel(str(path)+"/"+str(dir_list[file_name]),sheet_name=None, decimal=',',header=0)
    df_final_barrios = pd.DataFrame() 
         
    for district in distritos:
        #print("Distrito ", district)
        distrito_sheet_df  = df[district].iloc[rows_[anyo[file_name]], :]
        #df_indicadores = df.iloc[rows, :]
        #print(distrito_sheet_df.columns[1])
        categorias = ["Barrio","anyo","Distrito"]
        #categorias = list(df_indicadores[df_indicadores.columns[1]])
        if anyo[file_name] == 2020 or anyo[file_name] == 2021 or anyo[file_name] == 2022:
            categorias.extend(cambia_nombre_lista(list(distrito_sheet_df[distrito_sheet_df.columns[0]])))
            
            barrios = list(distrito_sheet_df.iloc[0,5:].dropna())
        else:
            categorias.extend(cambia_nombre_lista(list(distrito_sheet_df[distrito_sheet_df.columns[1]])))
            barrios = list(distrito_sheet_df.iloc[0,6:].dropna())
        
        categorias = list(filter(str.strip, categorias))
        categorias = list(map(str.strip, categorias))
        #barrios = list(distrito_sheet_df.iloc[0,6:18].dropna())
        df_transpose = distrito_sheet_df.T
         
        dict_indicadores = {}
        for row in range(1,len(distrito_sheet_df)):
                #print( row, " "+categorias[row+2])
                if anyo[file_name] == 2020 or anyo[file_name] == 2021 or anyo[file_name] == 2022:
                    df_aux =  distrito_sheet_df.iloc[row,5:]
                    
                else:
                    df_aux =  distrito_sheet_df.iloc[row,6:]
                #dict_indicadores[categorias[row+2]] = list(df_aux)
                if (categorias[row+2].strip() in index_elimina_nan) or (len(list(df_aux.dropna())) == len(barrios)):
                    aux_list = list(df_aux.dropna())
                    if len(aux_list) >  len(barrios):
                        delete_item = -(len(aux_list) - len(barrios))
                        aux_list = aux_list[:delete_item]
                    dict_indicadores[categorias[row+2]] = aux_list
                if (categorias[row+2].strip() in index_guardar_impares) and (len(list(df_aux.dropna())[1::2])== len(barrios)) :
                    aux_list = list(df_aux.dropna())[1::2]
                    if len(aux_list) >  len(barrios):
                        delete_item = -(len(aux_list) - len(barrios))
                        aux_list = aux_list[:delete_item]
                    dict_indicadores[categorias[row+2]] = aux_list
        dict_indicadores["Barrio"] = barrios
        dict_indicadores["anyo"] =  np.repeat(anyo[file_name],len(barrios))
        df_final_barrios = pd.concat([df_final_barrios, pd.DataFrame.from_dict(dict_indicadores)], ignore_index=True, sort=False)
    df_final_distritos =  pd.concat([df_final_distritos, df_final_barrios], ignore_index=True, sort=False)
df_final_anyo = pd.concat([df_final_anyo, df_final_distritos], ignore_index=True, sort=False)

# Se termina de solucionar el problema que estas dos colmunas
fix_density_col = list(df_final_anyo["Densidad (hab./Ha.)"].dropna())+list(df_final_anyo["Población densidad (hab./Ha.)"].dropna())
df_final_anyo["Densidad (hab./Ha.)"] = fix_density_col

# Se borran finalmente las columnas sin informacion y duplicadas
df_final_anyo = df_final_anyo.drop(columns=["Población densidad (hab./Ha.)","Superficie media de la vivienda (m2) en transacción"])

# Se ordena el dataframe segun el año y el barrio
df_final_anyo.sort_values(by=['Barrio', 'anyo'], ascending=[True, True], inplace=True)

#%%
df_general = pd.read_csv("DATOS/CLEAN/general_data.csv", sep=',', encoding='utf-8')

dfinal = df_general.merge(df_final_anyo, left_on=['Barrio', 'anyo'], right_on=['Barrio', 'Anyo'])


