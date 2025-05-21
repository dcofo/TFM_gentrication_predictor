# -*- coding: utf-8 -*-
"""

@author: nievesfo

Descripción: En este script se lleva a cabo el tratamiento de datos para añadir al archivo de indicadores:
    -Datos de nivel educativo de los residentes 
    -Precio de la vivienda nueva y de segunda mano
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

#%% FUNCIONES POR FICHERO

def extract_nivel_educativo_indicador(file):
    # Se carga el archivo y se renombran las columnas del año y del nombre del barrio
    df = pd.read_csv("DATOS/nivel_educativo.csv", sep=';', encoding='utf-8', skiprows=6)
    df = df.rename(columns={"Unnamed: 0": "anyo",
                            "Unnamed: 2": "Barrio"})
    # Se eliminan las últimas files que tenían valores nulos
    df = df.dropna()
    # Debido que que tenían un formato diferente, se tratan las columnas de barrio y anyo 
    # para que coincidan con el formato trabajado en este proyecto
    list_anyo = list(df["anyo"])
    list_barrio = []
    df["anyo"] = [item.split(' ')[4] for item in list_anyo]
    for item in list(df["Barrio"]):
        split_barrio = item.split('. ')
        if len(split_barrio) >1:
            list_barrio.append(split_barrio[1])
        else:
           list_barrio.append(split_barrio[0]) 
    df["Barrio"] = list_barrio
    
    # Se agrupan los niveles educativos en 3 categorias
    categoria_noEstudios = ["Sin estudios", "Enseñanza primaria incompleta"]
    categoria_estudiosMedios = ["Bachiller elemental, Graduado escolar, E.S.O.", "Formación profesional 1er grado", 
                  "Formación profesional 2º grado", "Bachiller superior, B.U.P.", "Otros titulados medios" ]
    categoria_estudioSuperior = ["Diplomado Escuela universitaria", "Arquitecto o Ingeniero técnico", 
                                 "Licenciado universitario, Arquitecto o Ingeniero", 
                                 "Doctorado o Estudios postgraduados"]
    # Dado que en este caso los puntos(.) son unidades de millar pero en código se interpretan como decimales,
    # se van a eliminar 
    for column in categoria_noEstudios+categoria_estudiosMedios+categoria_estudioSuperior:
        df[column] = df[column].astype(str).str.replace('.0', '').str.replace('.', '').astype("int")
        
    # Se crean 3 nuevas columnas donde se almacena la suma según la categoría    
    df['poblacion_noEstudios'] = df[categoria_noEstudios].sum(axis=1)
    df['poblacion_estudios_medios']= df[categoria_estudiosMedios].sum(axis=1)
    df['poblacion_estudios_superiores']= df[categoria_estudioSuperior].sum(axis=1)
    
    # Se crea dataframe con la selección de columnas y se resetea el indice
    df_selected = df[["anyo", "Barrio","poblacion_noEstudios","poblacion_estudios_medios", 
                     "poblacion_estudios_superiores"] ].sort_values(['anyo', 'Barrio'], ascending=[True, True]).reset_index(drop=True)
    
    
    set_list_anyo = set(list(df_selected["anyo"]))
    set_list_barrio = set(df_selected["Barrio"])
    # Se crea una columna con los tres valores formando un array
    df_selected['nivel_educativo_array'] = df_selected[['poblacion_noEstudios', 'poblacion_estudios_medios', 
                                                        'poblacion_estudios_superiores']].values.tolist()
    
    # Debido a que hay valores por distrito y ciudad se va a hacer la misma fórmula que para el resto:
    # crear un diccionario con los valores que luego se irán asignado fila a fila al dataframe general
    general_dict = {}
    for an in set_list_anyo:
        df_anyo_aux = df_selected.loc[df_selected['anyo'] == an]
        save_dict = {}
        for n_barrio in set_list_barrio:
            array_nivel_edcucativo = df_anyo_aux.loc[df_anyo_aux['Barrio'] == 
                                           n_barrio]['nivel_educativo_array'].reset_index(drop=True)[0]
            save_dict[n_barrio] = array_nivel_edcucativo
        general_dict[str(an)] = save_dict
     
    # Se carga el archivo de indicadores y se le añaden 3 columnas mas ne referencia al nivel de estudios
    df_general = pd.read_csv(file, sep=',', encoding='utf-8').sort_values(['anyo', 'Barrio'], ascending=[True, True])
    df_general['poblacion_noEstudios'] = 0
    df_general['poblacion_estudios_medios'] = 0
    df_general['poblacion_estudios_superiores'] = 0
    df_general['Barrio'] = df_general['Barrio'].str.replace('Concepción','La Concepción')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Villaverde Alto, Casco Histórico de Villaverde',
                                                              'Villaverde Alto - Casco Histórico de Villaverde')
           
    for anio in general_dict.keys():
        for barri in general_dict[anio].keys():
            df_general.loc[(df_general['anyo'] == int(anio)) & 
                           (df_general["Barrio"] == barri), 'poblacion_noEstudios'] =  int(general_dict[anio][barri][0])
            df_general.loc[(df_general['anyo'] == int(anio)) & 
                           (df_general["Barrio"] == barri), 'poblacion_estudios_medios'] =  int(general_dict[anio][barri][1])
            df_general.loc[(df_general['anyo'] == int(anio)) & 
                           (df_general["Barrio"] == barri), 'poblacion_estudios_superiores'] =  int(general_dict[anio][barri][2])
           

    return df_general

    
def extract_precio_vivienda_indicator(dataframe_general):
    df = pd.read_csv("DATOS/precio_vivienda_total.csv", sep=';', encoding='utf-8', skiprows=5)
    df = df.dropna()
    df = df.rename(columns={"2023": "2024",
                            "2022": "2023",
                            "2021": "2022",
                            "2020": "2021",
                            "2019": "2020",
                            "Unnamed: 1": "Barrio"})

    list_barrio = []

    for item in list(df["Barrio"]):
        split_barrio = item.split('. ')
        if len(split_barrio) >1:
            list_barrio.append(split_barrio[1])
        else:
           list_barrio.append(split_barrio[0]) 
            
    df["Barrio"] = list_barrio

    col_names_to_float = df.columns[2:]

    for column in col_names_to_float:
        df[column] = df[column].str.replace('.', '').str.replace(',', '.').astype(float)

    #df_final = pd.concat([df, df.loc[df.index.repeat(5)]], ignore_index=True).sort_values(['id'])
    df_final = pd.DataFrame()
    df_final_anyo = pd.DataFrame()
    for anyo in col_names_to_float:
        df_final["Barrio"] = df["Barrio"]
        df_final["anyo"] = int(anyo)
        df_final["precio vivienda (euros/m2)"] = df[anyo]
        df_final_anyo = pd.concat([df_final_anyo, df_final], ignore_index=True, sort=False)

    # Debido a que hay valores por distrito y ciudad se va a hacer la misma fórmula que para el resto:
    # crear un diccionario con los valores que luego se irán asignado fila a fila al dataframe general
    general_dict = {}
    for an in set(list(df_final_anyo["anyo"])):
        df_anyo_aux = df_final_anyo.loc[df_final_anyo['anyo'] == an]
        save_dict = {}
        for n_barrio in list_barrio:
            precio_vivienda = df_anyo_aux.loc[df_anyo_aux['Barrio'] == 
                                           n_barrio]["precio vivienda (euros/m2)"].reset_index(drop=True)[0]
            save_dict[n_barrio] = precio_vivienda
        general_dict[str(an)] = save_dict
        
    df_general = dataframe_general #pd.read_csv("DATOS/CLEAN/general_data.csv", sep=',', encoding='utf-8').sort_values(['anyo', 'Barrio'], ascending=[True, True])
    df_general['precio_vivienda'] = 0

            
    for anio in general_dict.keys():
        for barri in general_dict[anio].keys():
            df_general.loc[(df_general['anyo'] == int(anio)) & 
                            (df_general["Barrio"] == barri), 'precio_vivienda'] =  general_dict[anio][barri]
    return df_general
    

#%% MAIN

if __name__ == '__main__':
    path = 'DATOS/CLEAN/'
    file = "general_data_v2.csv"
    df_nivel_educativo = extract_nivel_educativo_indicador(path+file)
    df_precio_vivienda = extract_precio_vivienda_indicator(df_nivel_educativo)
    df_precio_vivienda["anyo_timestamp"] = pd.to_datetime(df_precio_vivienda['anyo'], format='%Y').dt.strftime('%Y-%m-%d')
    clean_and_select_places.create_csv(df_precio_vivienda, path, "general_data_v3.csv")
    print("main")



