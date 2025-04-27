# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 20:09:03 2025

@author: Nievesita
"""

# Se va a añadir una columna donde anyo se va a poner en formato timestamp
# de forma que se cargue correctamente en CARTO

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

#%% HECHO
df = pd.read_csv("DATOS/CLEAN/general_data_v1.csv", sep=',', encoding='utf-8')

df["anyo_timestamp"] = pd.to_datetime(df['anyo'], format='%Y').dt.strftime('%Y-%m-%d')

clean_and_select_places.create_csv(df, 'DATOS/CLEAN/', "general_data_timestamp.csv")


# %% HECHO
df_act_eco = pd.read_csv("DATOS/CLEAN/Actividad_economica/actividad_economica_concat_files_v1.csv", sep=',',encoding='latin-1')
df_dele = df_act_eco.dropna()
df_rename = df_dele.rename(columns={"rotulo": "nombre", 
                                 "desc_seccion": "actividad_general",
                                 "desc_division":"actividad_concreta",
                                 "desc_epigrafe":"actividad_en_detalle"})
df_rename = df_rename.drop(columns=['desc_barrio_local.1'])
df_rename["anyo_timestamp"] = pd.to_datetime(df_rename['anyo'], format='%Y').dt.strftime('%Y-%m-%d')
clean_and_select_places.create_csv(df_rename, 'DATOS/CLEAN/Actividad_economica/', "actividad_economica_concat_files_timestamp.csv")

#%% HECHO
#print(df_rename.columns)

df_airbnb = pd.read_csv("DATOS/CLEAN/airbnb_clean.csv",  sep=',', encoding='utf-8')
df_airbnb["anyo_timestamp"] = pd.to_datetime(df_airbnb['anyo'], format='%Y').dt.strftime('%Y-%m-%d')
clean_and_select_places.create_csv(df_airbnb, 'DATOS/CLEAN/', "airbnb_clean_timestamp.csv")

#%% HECHO

df_inversion = pd.read_csv("DATOS/CLEAN/INVERSIONES/full_inversiones20-25.csv",  sep=',', encoding='utf-8')
df_inversion["anyo_timestamp"] = pd.to_datetime(df_inversion['anyo'], format='%Y').dt.strftime('%Y-%m-%d')
clean_and_select_places.create_csv(df_inversion, 'DATOS/CLEAN/INVERSIONES/', "full_inversiones20-25_timestamp.csv")

