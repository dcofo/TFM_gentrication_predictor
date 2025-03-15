# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 23:57:16 2024

@author: Nieves Fernández Ochoa

Descripción: Script para limpieza de datos de lugares

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
#geolocator = Photon(user_agent="measurements")
#location = geolocator.reverse(Latitude+","+Longitude)

#%% FUNCIONES AUXILIARES

def load_csv(folder, file):
    # Se carga el archivo en formato pandas 
    df = pd.read_csv(str(folder)+"/"+str(file)+".csv")
    return df

def remove_duplicates(dataframe):
    return dataframe.drop_duplicates()

def remove_empty_neighbor(daframe):
    return daframe[daframe.barrio != "None"]

def fix_puntuation_problems(daframe):
    # hacer mas adelante
    return daframe
    

def create_csv(dataframe, directory, file_name):
    dataframe.to_csv(directory+file_name, index=False)  

def clean_actividad_economica():
    path = "DATOS/Actividad_economica"
    anyo = list(range(2018,2025))
    sel_columns = ["rotulo", "id_distrito_local", "desc_barrio_local", "id_barrio_local", "desc_barrio_local", "coordenada_x_local",
                      "coordenada_y_local", "desc_seccion", "desc_division", "desc_epigrafe"]
    dir_list = os.listdir(path)
    #df_append = pd.DataFrame()
    for file_name in range(len(dir_list)):
        print("Reading ", dir_list[file_name])
        df = pd.read_csv(str(path)+"/"+str(dir_list[file_name]), index_col=0, sep=';', encoding='latin-1')
        df_selected = df[sel_columns]
        df_selected["anyo"] = anyo[file_name]
        df_selected_drop = df_selected.drop_duplicates()
        df_selected_drop["coordenada_x_local"] = df_selected_drop["coordenada_x_local"].str.replace(',', '.').astype(float)
        df_selected_drop["coordenada_y_local"] = df_selected_drop["coordenada_y_local"].str.replace(',', '.').astype(float)
        df_selected_drop["coordenada_x_local"] = pd.to_numeric(df_selected_drop["coordenada_x_local"])
        df_selected_drop["coordenada_y_local"] = pd.to_numeric(df_selected_drop["coordenada_y_local"])
        # Delete rows with 0
        df_selected_drop = df_selected_drop.loc[(df_selected_drop["coordenada_x_local"] != 0) &   (df_selected_drop["coordenada_y_local"] != 0) ]
        # Create new columns
        df_selected_drop["latitude"], df_selected_drop["longitude"] = utm.to_latlon(df_selected_drop["coordenada_x_local"], df_selected_drop["coordenada_y_local"], 30, 'T')
        #df_append = df_selected_drop.append(df_append, ignore_index=True)
        #df_append = df_selected_drop.merge(df_append, on = sel_columns[1], how = 'outer')
        # Se crea un nuevo csv 
        df_selected_drop.to_csv('DATOS/CLEAN/Actividad_economica/'+str(dir_list[file_name]), index=False)  

def clean_alojamiento_turisticos_XML():
    path = "DATOS"
    

def utm_to_latlon(dataframe):
    #utm.to_latlon(442316.074, 4475353.583, 30, 'T')
    lat, lon = utm.to_latlon(dataframe["coordenada_x_local"], dataframe["coordenada_y_local"], 30, 'T')
    return pd.Series({"lat": lat, "long": lon})
#df.merge(df.apply(rule, axis=1), left_index= True, right_index= True)

def latlon_to_utm(Latitude, Longitude):
    coords = utm.from_latlon(float(Latitude), float(Longitude))
    return coords

# Función para convertir en polígonos los arrays de coordenadas
def get_polygon(list_coords):
    point_list = [Point(y,x) for [x,y] in list_coords]
    # Con todos los puntos se forman poligonos
    polygon_feature = Polygon([[poly.x, poly.y] for poly in point_list])
    return polygon_feature

def check_barrio(polys_json, latitud, longitud):
    p = Point(latitud, longitud)
    for poligon in range(len(polys_json["coordinates"])):
        if p.within(polys_json["coordinates"][poligon]) == True:
            return polys_json["nombre_barrio"][poligon]

def join_files(path,filename):
    dir_list = os.listdir(path)
    df_concat = pd.concat([pd.read_csv(f) for f in dir_list ], ignore_index=True)
    df_concat.to_csv(path+'/'+filename+'_concat_files.csv', index=False)
'''
def get_limite_barrios():
    # Se carga y se tratan los datos referentes a los límites de los barrios
    path = "DATOS/Límites de los Barrios Administrativos de Madrid.geojson"
    file = open(path)
    # Se carga el archivo como geopandas
    polys_json = gpd.read_file(file, driver='GeoJSON')
    polys_json['coordinates'] = polys_json['coordinates'].str[1:-1].apply(literal_eval)
    
    # Se aplica la funcion a la columna de coordenadas
    polys_json['coordinates'] = polys_json['coordinates'].apply(get_polygon)
    
    centroid_barrios_path = "DATOS/centroid_barrios.csv"
    neighbo = pd.read_csv(centroid_barrios_path, sep=',', encoding='latin-1',on_bad_lines='skip', float_precision='round_trip')
    lati = list(neighbo["Latitude"])
    longi = list(neighbo["Longitude"])
    barris = list(neighbo['Name'])

    # Se recorren cada poligono para etiquetar el nombre del barrio correctamente segun el calculo del centroide
    array_cent = []
    array_order_barri = []
    for poligon in polys_json["coordinates"]:
        cent = poligon.centroid
        array_cent.append(cent.wkt)
        for sel in range(len(lati)):
            if lati[sel] == cent.x:
                if longi[sel] == cent.y:
                    array_order_barri.append(barris[sel])
                    break
    polys_json["nombre_barrio"] = array_order_barri
    return polys_json
    
'''

#%% FUNCIONES PARA TRATAMIENTO CONCRETO DE LIMPIEZA DE ARCHIVOS

def get_limite_barrios():
    # Se carga y se tratan los datos referentes a los límites de los barrios
    path = "DATOS/Límites de los Barrios Administrativos de Madrid.geojson"
    file = open(path)
    # Se carga el archivo como geopandas
    polys_json = gpd.read_file(file, driver='GeoJSON')
    polys_json['coordinates'] = polys_json['coordinates'].str[1:-1].apply(literal_eval)
    
    # Se aplica la funcion a la columna de coordenadas
    polys_json['coordinates'] = polys_json['coordinates'].apply(get_polygon)
    
    # Se cargan las coordenadas del centro de cada barrio
    centroid_barrios_path = "DATOS/centroid_barrios.csv"
    neighbo = pd.read_csv(centroid_barrios_path, sep=',', encoding='latin-1',on_bad_lines='skip', float_precision='round_trip')
    lati = list(neighbo["Latitude"])
    longi = list(neighbo["Longitude"])
    barris = list(neighbo['Name'])

    # Se recorren cada poligono para etiquetar el nombre del barrio correctamente segun el calculo del centroide
    array_cent = []
    array_order_barri = []
    for poligon in polys_json["coordinates"]:
        # Se calcula el centroide del poligono
        cent = poligon.centroid
        array_cent.append(cent.wkt)
        for sel in range(len(lati)):
            if lati[sel] == cent.x:
                if longi[sel] == cent.y:
                    array_order_barri.append(barris[sel])
                    break
    polys_json["nombre_barrio"] = array_order_barri
    return polys_json

def clean_xml_files(polys_json, file_name):
    # Se carga el archivo XML
    df_xml = ET.parse(file_name)
    root = df_xml.getroot()
    # Inicialización de variables 
    anyo_xml = []
    nombre_xml = []
    long_xml = []
    latit_xml = []
    general_acti_xml = []
    activ_detallada_xml = []
    barrio_xml =  []
    array_utm_x = []
    array_utm_y = []
    df_clean_xml = pd.DataFrame()
    
    # Se parsea el archivo XML
    for serv in root.findall("service"):
        anyo_xml.append(serv.attrib['fechaActualizacion'].split('-')[0])
        nombre_xml.append(serv[0][1].text)
        latit_xml.append(float( serv[1][4].text))
        long_xml.append(float(serv[1][5].text))
        coords_utm = latlon_to_utm(float(serv[1][4].text), float(serv[1][5].text))
        array_utm_x.append(coords_utm[0])
        array_utm_y.append(coords_utm[1])
        general_acti_xml.append(serv[3][1].text)
        # En caso de que no exista la categoria se deja en blanco
        try:
            activ_detallada_xml.append( serv[3][2].find('.//categoria')[1].text)
        except:
            activ_detallada_xml.append('-')
    # Se busca el barrio al que pertenece escaneando las coordenadas en la funcion creada
    for ele in range(len(long_xml)):
        barrio_xml.append(check_barrio(polys_json, latit_xml[ele], long_xml[ele]))

    # Se guarda toda la información en el dataframe alojamiento_hotelero
    df_clean_xml['nombre'] = nombre_xml
    df_clean_xml['barrio'] = barrio_xml
    df_clean_xml['coord_x_utm'] = array_utm_x
    df_clean_xml['coord_y_utm'] = array_utm_y
    df_clean_xml['latitude'] = latit_xml
    df_clean_xml['longitude'] = long_xml
    df_clean_xml['actividad_general'] = general_acti_xml
    df_clean_xml['actividad_detallada'] = activ_detallada_xml
    df_clean_xml['anyo'] = anyo_xml
    
    # Se eliminan las entradas que no tienen un barrio asociado valido
    
    return df_clean_xml


#%%

if __name__ == '__main__':
    #clean_actividad_economica()
    barrios_en_poligonos_data = get_limite_barrios()
    xml_files = ["alojamientos_v1_es", 'turismo_v1_es']
    for file in xml_files:
        print("Reading ", file)
        data_to_csv_from_xml = clean_xml_files(barrios_en_poligonos_data, "DATOS/"+file+".xml") 
        create_csv(data_to_csv_from_xml, 'DATOS/CLEAN/',  file+"_clean")
    print("main")
    
#%% PRUEBAS

# Se carga y se tratan los datos referentes a los límites de los barrios
path = "DATOS/Límites de los Barrios Administrativos de Madrid.geojson"
file = open(path)
# Se carga el archivo como geopandas
polys_json = gpd.read_file(file, driver='GeoJSON')
polys_json['coordinates'] = polys_json['coordinates'].str[1:-1].apply(literal_eval)

# Función para convertir en politicos arrays de coordenadas
def get_polygon(list_coords):
    point_list = [Point(y,x) for [x,y] in list_coords]
    # Con todos los puntos se forman poligonos
    polygon_feature = Polygon([[poly.x, poly.y] for poly in point_list])
    return polygon_feature

# Se aplica la funcion a la columna de coordenadas
polys_json['coordinates'] = polys_json['coordinates'].apply(get_polygon)

centroid_barrios_path = "DATOS/centroid_barrios.csv"
neighbo = pd.read_csv(centroid_barrios_path, sep=',', encoding='latin-1',on_bad_lines='skip', float_precision='round_trip')
lati = list(neighbo["Latitude"])
longi = list(neighbo["Longitude"])
barris = list(neighbo['Name'])

# Se recorren cada poligono para etiquetar el nombre del barrio correctamente segun el calculo del centroide
array_cent = []
array_order_barri = []
for poligon in polys_json["coordinates"]:
    cent = poligon.centroid
    array_cent.append(cent.wkt)
    for sel in range(len(lati)):
        if lati[sel] == cent.x:
            if longi[sel] == cent.y:
                array_order_barri.append(barris[sel])
                break
polys_json["nombre_barrio"] = array_order_barri



        