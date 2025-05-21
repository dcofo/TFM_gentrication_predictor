# -*- coding: utf-8 -*-
"""
@author: nievesfo

Descripción: Script que limpieza y transforma los datos de las inversiones aprobadas 
            por el gobierno municipal desde 2020 a 2024
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

def clean_numeric_column(x):
    split_x = x.split('.')
    split_x_float= float(''.join(split_x).replace(',', '.'))
    return split_x_float
    

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
        
        # Se corrigen los nombres de los barrios
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Palos de Moguer', 'Palos de la Frontera')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Rios Rosas','Ríos Rosas')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Salvador','El Salvador')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Los Jeronimos','Los Jerónimos')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('San Andrés',
                                                                                         'Villaverde Alto, Casco Histórico de Villaverde')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Los Angeles','Ángeles')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('San Cristobal','San Cristóbal')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Casco histórico de Vicálvaro','Casco Histórico de Vicálvaro')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('LOS CARMENES','Los Cármenes')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Fuentelareina','Fuentelarreina')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Aguilas','Águilas')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Apostol Santiago','Apóstol Santiago')
        df_selected_drop['Denominacion Barrio'] = df_selected_drop['Denominacion Barrio'].str.replace('Puerta del Angel','Puerta del Ángel')
        
        # Se genera el csv limpio
        outdir_inv = 'DATOS/CLEAN/INVERSIONES/'
        if not os.path.exists(outdir_inv):
            os.mkdir(outdir_inv)
        clean_and_select_places.create_csv(df_selected_drop, outdir_inv, dir_list[file_name])
        

def agrupaInversiones(df_general):
    # Se abre los nuevos archivos limpios
    path = "DATOS/CLEAN/INVERSIONES"
    dir_list = os.listdir(path)
    df_full_inversiones = pd.DataFrame()
    list_barrio = []
    df_general["Inversion"] = 0
    for file_name in range(len(dir_list)):
        print("Reading cleaned ", dir_list[file_name])
        df = pd.read_csv(str(path)+"/"+str(dir_list[file_name]), sep=',', encoding='utf-8')
        # En caso de que no se haya detectado correctamente algún barrio
        df = df.dropna()
        # Se añade columna timestamp
        df["anyo_timestamp"] = pd.to_datetime(df['anyo'], format='%Y').dt.strftime('%Y-%m-%d')
        # Vamos a agrupar tambien todas las inversiones en un único Dataframe para poder 
        # sacar algo de conocimiento previo
        df_full_inversiones = pd.concat([df_full_inversiones, df], ignore_index=True, sort=False)
        # Se agrupan en listas los barrios
        list_barrio = list(df["Denominacion Barrio"])
        tipos_inv = set(list(df["DENOMINACIÓN LÍNEA DE INVERSIÓN"]))
        # Se transforma la columna
        df["Total previsto"] = df["Total previsto"].apply(clean_numeric_column)
        for ele_barrio in list_barrio:
                aux_df = df.loc[(df["Denominacion Barrio"] == ele_barrio)]
                anyo_inv = aux_df.iloc[0, aux_df.columns.get_loc("anyo")]
                sum_inversion = aux_df["Total previsto"].sum()
                # Se busca el año y el barrio en el df_general y se le asigna nuevo valor a la inversion
                df_general.loc[(df_general['anyo'] == anyo_inv) & (df_general["Barrio"] == ele_barrio), 'Inversion'] = sum_inversion
    return df_full_inversiones, df_general

def crear_archivo_global():
    barrios_df = clean_and_select_places.get_limite_barrios()
    nombre_barrios = list(barrios_df["nombre_barrio"])
    anyos = list(range(2020,2025))
    # Se crea el dataframe
    barrios = np.tile(nombre_barrios, len(anyos))
    anyo_rep = np.repeat(anyos, len(nombre_barrios))
    df_general = pd.DataFrame({"Barrio": barrios, "anyo": anyo_rep})
    
    # Se corrigen los nombres de los barrios
    df_general['Barrio'] = df_general['Barrio'].str.replace('Palos de Moguer', 'Palos de la Frontera')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Rios Rosas','Ríos Rosas')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Salvador','El Salvador')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Jerónimos','Los Jerónimos')
    df_general['Barrio'] = df_general['Barrio'].str.replace('San Andrés', 'Villaverde Alto, Casco Histórico de Villaverde')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Los Angeles','Ángeles')
    df_general['Barrio'] = df_general['Barrio'].str.replace('San Cristobal','San Cristóbal')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Casco histórico de Vicálvaro','Casco Histórico de Vicálvaro')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Cármenes','Los Cármenes')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Fuentelareina','Fuentelarreina')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Aguilas','Águilas')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Apostol Santiago','Apóstol Santiago')
    df_general['Barrio'] = df_general['Barrio'].str.replace('Puerta del Angel','Puerta del Ángel')
    return df_general
    

#%%

if __name__ == '__main__':
    df_general = crear_archivo_global()
    select_and_clean_inversiones()
    df_full_inversiones, df_general = agrupaInversiones(df_general)
    print("Creating full_inversiones20-25 csv...")
    clean_and_select_places.create_csv(df_full_inversiones, 'DATOS/CLEAN/INVERSIONES/', "full_inversiones20-25_timestamp.csv")
    print("Creating general_data csv...")
    clean_and_select_places.create_csv(df_general, 'DATOS/CLEAN/', "general_data.csv")
    print("main")
    

        
