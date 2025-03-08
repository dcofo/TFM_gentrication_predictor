# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 15:48:42 2025

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
'''
Los valores de latitud y longitud poseen un formato erróneo, 
si se limpian y se afinan correctamente, podrán servir para identificar 
el barrio gracias a la función desarrollada
'''
def clean_long_lat_values(lat_list, long_list):
    # Coordenadas de Madrid son en torno a 40.4165, -3.70256
    for ele in range(len(lat_list)):
        # Transformacion para los valores de latitud        
        split_lati = lat_list[ele].split(".")
        if len(split_lati) <=2:
            split_lati2 = split_lati[0]+split_lati[1]
        else:
            split_lati2 = split_lati[0]+split_lati[1]+split_lati[2]
        lat_list[ele] = float(split_lati2[:2] + '.' + split_lati2[2:])
        
        # Transformacion para los valores de longitud
        split_long = str(long_list[ele]).split(".")
        if len(split_long) <=2:
            split_long2 = split_long[0]+split_long[1]
        else:
            split_long2 = split_long[0]+split_long[1]+split_long[2]
        long_list[ele] = float(split_long2[:2] + '.' + split_long2[2:])
    return lat_list, long_list
        
    

#%%
#INVERSIONES
def select_and_clean_inversiones():
    path = "DATOS/INVERSIONES"
    anyo = list(range(2020,2025))
    # Necesario aplicar de nuevo la función para etiquetar el nombre del barrio
    polys_json = clean_and_select_places.get_limite_barrios()
    sel_columns = ["Denominación Distrito", "Latitud", "Longitud", "DENOMINACIÓN LÍNEA DE INVERSIÓN", "Total previsto"]
    dir_list = os.listdir(path)
    for file_name in range(len(dir_list)):
        # Listas auxiliares
        etiqueta_barrio = []
        array_utm_x = []
        array_utm_y = []
        print("Reading ", dir_list[file_name])
        df = pd.read_csv(str(path)+"/"+str(dir_list[file_name]), index_col=0, sep=';', encoding='utf-8')        
        df_selected = df[sel_columns]
        df_selected = df_selected.dropna()
        df_selected["anyo"] = anyo[file_name]

        # Se eliminan filas duplicadas
        df_selected_drop = df_selected.drop_duplicates()
        
        # Para trabajar correctamente con los valores se transforman en lista y se limpian previamente
        # ya que hay archivos con mal formato
        if anyo[file_name] == 2023 or anyo[file_name] == 2022:
            lat_list,lon_list = clean_long_lat_values(list(df_selected_drop["Latitud"]),list(df_selected_drop["Longitud"]))
        else:
            if anyo[file_name] == 2021:
                df_selected_drop['Latitud'] = df_selected_drop['Latitud'].str[1:]
                df_selected_drop['Longitud'] = df_selected_drop['Longitud'].str[1:]
            lat_list,lon_list = list(df_selected_drop["Latitud"]),list(df_selected_drop["Longitud"])
        
        for ele in range(len(lat_list)):
            etiqueta_barrio.append(clean_and_select_places.check_barrio(polys_json, float(lat_list[ele]), float(lon_list[ele])))
            try:
                utm__coords = clean_and_select_places.latlon_to_utm(lat_list[ele], lon_list[ele])
            except Exception:
                print("ERROR en la traducción a coordenadas UTM")

            array_utm_x.append(utm__coords[0])
            array_utm_y.append(utm__coords[1])
        df_selected_drop["Denominacion Barrio"] = etiqueta_barrio
        df_selected_drop["coord_x_UTM"] = array_utm_x
        df_selected_drop["coord_y_UTM"] = array_utm_y
        df_selected_drop["Latitud"] = lat_list
        df_selected_drop["Longitud"] = lon_list
        
        
        # Se genera el csv limpio
        clean_and_select_places.create_csv(df_selected_drop, dir_list[file_name]+"nuevo")

#%%

if __name__ == '__main__':
    select_and_clean_inversiones()
    print("main")
    

     


#%%
#2022_Inversiones_Principales  / 2021_GeolocalizacionInversiones
etiqueta_barrio = []
polys_json = clean_and_select_places.get_limite_barrios()
df = pd.read_csv(str(path)+"/2023_Inversiones_Principales.csv", index_col=0, sep=';', encoding='utf-8')
df_selected = df[sel_columns]
df_selected = df_selected.dropna()
df_selected["anyo"] = anyo[file_name]
df_selected_drop = df_selected.drop_duplicates()
#df_selected_drop['Latitud'] = df_selected_drop['Latitud'].str[1:]
#df_selected_drop["Latitud"] = pd.to_numeric(df_selected_drop["Latitud"])
#df_selected_drop["Longitud"] = pd.to_numeric(df_selected_drop["Longitud"])



lat_list = list(df["Latitud"])
lon_list = list(df["Longitud"])

for ele in range(len(df["Latitud"])):
    # Transformacion para los valores de latitud
    split_lati = lat_list[ele].split(".")
    split_lati2 = split_lati[0]+split_lati[1]
    lat_list[ele] = float(split_lati2[:2] + '.' + split_lati2[2:])
    # Transformacion para los valores de longitud
    split_long = lon_list[ele].split(".")
    split_long2 = split_long[0]+split_long[1]
    lon_list[ele] = float(split_long2[:2] + '.' + split_long2[2:])
    
print(lat_list,lon_list )

#lat_list,lon_list = list(df_selected_drop["Latitud"]),list(df_selected_drop["Longitud"])

for ele in range(len(lat_list)):
    etiqueta_barrio.append(clean_and_select_places.check_barrio(polys_json, float(lat_list[ele]), float(lon_list[ele])))
    try:
        utm__coords = clean_and_select_places.latlon_to_utm(lat_list[ele], lon_list[ele])
    except Exception:
        print(" ERROR")
        print(lat_list[ele], lon_list[ele])        
        
