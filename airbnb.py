# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 00:15:13 2025

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

#%%

def alquiler_vacacional_info():
    path = "DATOS"
    df = pd.read_csv("DATOS/airbnb.csv", sep=',', encoding='utf-8')
    df_clean = df.dropna(subset=['first_review', 'last_review', 'neighbourhood_cleansed'],ignore_index=True)

    # Seleccion de columnas
    sel_columns = ['id', 'neighbourhood_cleansed', 'latitude', 'longitude','first_review','last_review' ]
    df_sel_clean = df_clean[sel_columns].sort_values(['id'], ignore_index=True)
    # Creación de columnas en coordenadas UTM
    lat_list = list(df_sel_clean['latitude'])
    lon_list = list(df_sel_clean['longitude'])
    coord_list_x = []
    coord_list_y = []
    for row in range( len(df_sel_clean)):
        coords_utm = clean_and_select_places.latlon_to_utm(float(lat_list[row]), float(lon_list[row]))
        coord_list_x.append(coords_utm[0])
        coord_list_y.append(coords_utm[1])
    # Se crean las columnas del dataframe con las coordenadas UTM
    df_sel_clean['coord_x_utm'] = coord_list_x
    df_sel_clean['coord_y_utm'] = coord_list_y
    
    copies = []
    list_anyo = []
    for ele in range(len(df_sel_clean)):
        start_date = int(df_sel_clean.loc[ele]['first_review'].split('-')[0])
        last_date = int(df_sel_clean.loc[ele]['last_review'].split('-')[0])
        year_array = list(range(start_date,last_date+1))
        list_anyo = list_anyo + year_array
        number_of_extra_copies = last_date - start_date
        copies.append(number_of_extra_copies)
    df_sel_clean["n_copy"] = copies
    df_final = pd.concat([df_sel_clean, df_sel_clean.loc[df_sel_clean.index.repeat(df_sel_clean.n_copy)]], ignore_index=True).sort_values(['id'])
    df_final["anyo"] = list_anyo
    df_final["anyo"] = pd.Timestamp(df_final.anyo, format='%Y')
    df_final = df_final.drop(columns = ['n_copy'])
    return df_final

def extract_indicator_piso_turistico(dataframe):
    # Los indicadores van de 2020 a 2024 por lo que primero se hará una selección de esos años
    df_anyo = df_airbnb.loc[(df_airbnb['anyo'] == 2020) | (df_airbnb['anyo'] == 2021) |
                            (df_airbnb['anyo'] == 2022) | (df_airbnb['anyo'] == 2023) |
                            (df_airbnb['anyo'] == 2024) ]
    anyo = set(list(df_anyo['anyo']))
    barrio = sorted(set(list(df_anyo['neighbourhood_cleansed'])))
    general_dict = {}
    for an in anyo:
        df_anyo_aux = df_anyo.loc[df_anyo['anyo'] == an]
        save_dict = {}
        for n_barrio in barrio:
            cuenta_pisos = len(df_anyo_aux.loc[df_anyo_aux['neighbourhood_cleansed'] == n_barrio])
            save_dict[n_barrio] = cuenta_pisos
        general_dict[str(an)] = save_dict

    # se abre el csv de indicadores
    df_general = pd.read_csv("DATOS/CLEAN/general_data.csv", sep=',', encoding='utf-8') 

    # se crea una columna nueva todo a 0
    df_general["airbnb"] = 0
    # se le van asignando los datos en funcion del año y del barrio
    for year in general_dict.keys():
        for barri in general_dict[year].keys():
            df_general.loc[(df_general['anyo'] == int(year)) & (df_general["Barrio"] == barri), 'airbnb'] = int(general_dict[year][barri])
    return df_general

#%%
if __name__ == '__main__':
    df_airbnb = alquiler_vacacional_info()
    clean_and_select_places.create_csv(df_airbnb, 'DATOS/CLEAN/', "airbnb_clean.csv")
    indicator_piso_turistico = extract_indicator_piso_turistico(df_airbnb)
    clean_and_select_places.create_csv(indicator_piso_turistico, 'DATOS/CLEAN/', "general_data_v1.csv")
    
#%%
path = "DATOS"
df = pd.read_csv("DATOS/airbnb.csv", sep=',', encoding='utf-8')
df_clean = df.dropna(subset=['first_review', 'last_review', 'neighbourhood_cleansed'],ignore_index=True)
sel_columns = ['id', 'neighbourhood_cleansed', 'latitude', 'longitude','first_review','last_review' ]
df_sel_clean = df_clean[sel_columns]
lat_list = list(df_sel_clean['latitude'])
lon_list = list(df_sel_clean['longitude'])
coord_list_x = []
coord_list_y = []
for row in range( len(df_sel_clean)):
    coords_utm = clean_and_select_places.latlon_to_utm(float(lat_list[row]), float(lon_list[row]))
    coord_list_x.append(coords_utm[0])
    coord_list_y.append(coords_utm[1])
# Se crean las columnas del dataframe con las coordenadas UTM
df_sel_clean['coord_x_utm'] = coord_list_x
df_sel_clean['coord_y_utm'] = coord_list_y

#print(df_sel_clean["neighbourhood_cleansed"].value_counts())

#%%
fi = '2023-08-12'
la = '2024-09-08'

fi_spli = int(fi.split('-')[0])
la_split = int(la.split('-')[0])

dif = la_split-fi_spli
prueba =list(range(fi_spli,la_split+1))

df_prueba = df_sel_clean.loc[0:3].sort_values(['id'], ignore_index=True)
copies = []
list_anyo = []
for ele in range(len(df_prueba)):
    start_date = int(df_prueba.loc[ele]['first_review'].split('-')[0])
    last_date = int(df_prueba.loc[ele]['last_review'].split('-')[0])
    year_array = list(range(start_date,last_date+1))
    list_anyo = list_anyo + year_array
    number_of_extra_copies = last_date - start_date
    copies.append(number_of_extra_copies)
df_prueba["n_copy"] = copies
df_prueba1 = pd.concat([df_prueba, df_prueba.loc[df_prueba.index.repeat(df_prueba.n_copy)]], ignore_index=True).sort_values(['id'])
df_prueba1["anyo"] = list_anyo

#%%

df_anyo = df_airbnb.loc[(df_airbnb['anyo'] == 2020) | (df_airbnb['anyo'] == 2021) |
                        (df_airbnb['anyo'] == 2022) | (df_airbnb['anyo'] == 2023) |
                        (df_airbnb['anyo'] == 2024) ]
anyo = set(list(df_anyo['anyo']))
barrio = sorted(set(list(df_anyo['neighbourhood_cleansed'])))
general_dict = {}
for an in anyo:
    df_anyo_aux = df_anyo.loc[df_anyo['anyo'] == an]
    save_dict = {}
    for n_barrio in barrio:
        cuenta_pisos = len(df_anyo_aux.loc[df_anyo_aux['neighbourhood_cleansed'] == n_barrio])
        save_dict[n_barrio] = cuenta_pisos
    general_dict[str(an)] = save_dict

# se abre el csv de indicadores
df_general = pd.read_csv("DATOS/CLEAN/general_data.csv", sep=',', encoding='utf-8') 

# se crea una columna nueva todo a 0
df_general["airbnb"] = 0
# se le van asignando los datos en funcion del año y del barrio
for year in general_dict.keys():
    for barri in general_dict[year].keys():
        print("pisos ",  general_dict[year][barri] )
        df_general.loc[(df_general['anyo'] == int(year)) & (df_general["Barrio"] == barri), 'airbnb'] = int(general_dict[year][barri])           
# Se guarda

#%%
#print(df_general[""])
print(df_general.loc[(df_general['anyo'] == 2020) & (df_general["Barrio"] == "Abrantes"), 'airbnb'] )

df_general.loc[(df_general['anyo'] == 2020) & (df_general["Barrio"] == "Abrantes"), 'airbnb'] = 666
print(general_dict['2020']['Abrantes'])