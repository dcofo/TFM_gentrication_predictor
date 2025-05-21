# -*- coding: utf-8 -*-
"""
ARCHIVO AUXILIAR

@author: nievesfo
"""
# se cambia el formato del archivo general para flourish

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
df_general = pd.read_csv("DATOS/CLEAN/general_data_v3.csv", sep=',', encoding='utf-8') 
categorias_col_name = df_general.columns[2:]

df_2020 = pd.DataFrame()
df_2020 = df_general.loc[df_general["anyo"] == 2020]
barrios = sorted(list(set(list(df_2020["Barrio"]))),reverse=False)

df_2020 = df_2020[categorias_col_name].transpose()
for col_name in range(len(barrios)):
    df_2020 = df_2020.rename(columns={col_name: barrios[col_name]})

df_2020 = df_2020.reset_index()
df_2020["anyo"] = 2020
df_2020_col_name = df_2020.columns
print("pues paso 1")


df_prueba = pd.DataFrame()
df_prueba["categoria"] = categorias_col_name
df_prueba["anyo"] = 2020

# %%

df_2021 = pd.DataFrame()
df_2021 = df_general.loc[df_general["anyo"] == 2021].reset_index(drop=True)
barrios = sorted(list(set(list(df_2021["Barrio"]))),reverse=False)

df_2021 = df_2021[categorias_col_name].transpose()
for col_name in range(len(barrios)):
    df_2021 = df_2021.rename(columns={col_name: barrios[col_name]})

df_2021 = df_2021.reset_index()
df_2021["anyo"] = 2021
df_2021_col_name = df_2021.columns

#%%

df_2022 = pd.DataFrame()
df_2022 = df_general.loc[df_general["anyo"] == 2022].reset_index(drop=True)
barrios = sorted(list(set(list(df_2022["Barrio"]))),reverse=False)

df_2022 = df_2022[categorias_col_name].transpose()
for col_name in range(len(barrios)):
    df_2022 = df_2022.rename(columns={col_name: barrios[col_name]})

df_2022 = df_2022.reset_index()
df_2022["anyo"] = 2022

df_2022_col_name = df_2022.columns

#%%
df_2023 = pd.DataFrame()
df_2023 = df_general.loc[df_general["anyo"] == 2023].reset_index(drop=True)
barrios = sorted(list(set(list(df_2023["Barrio"]))),reverse=False)

df_2023 = df_2023[categorias_col_name].transpose()
for col_name in range(len(barrios)):
    df_2023 = df_2023.rename(columns={col_name: barrios[col_name]})

df_2023 = df_2023.reset_index()
df_2023["anyo"] = 2023

df_2023_col_name = df_2023.columns


#%%

df_2024 = pd.DataFrame()
df_2024 = df_general.loc[df_general["anyo"] == 2024].reset_index(drop=True)
barrios = sorted(list(set(list(df_2024["Barrio"]))),reverse=False)

df_2024 = df_2024[categorias_col_name].transpose()
for col_name in range(len(barrios)):
    df_2024 = df_2024.rename(columns={col_name: barrios[col_name]})

df_2024 = df_2024.reset_index()
df_2024["anyo"] = 2024

df_2024_col_name = df_2024.columns

#%%
df_flourish =  pd.concat([df_2020, df_2021,df_2022,df_2023,df_2024], ignore_index=True, sort=False)
#para csv
clean_and_select_places.create_csv(df_flourish, 'DATOS/CLEAN/', "flourish_indicadores.csv")
#df_flourish = df_flourish.dropna(axis=1)


#%% data para radares

df_acticidad = pd.read_csv("DATOS/CLEAN/Actividad_economica2/actividad_economica_concat_files_timestamp.csv", sep=',', encoding='utf-8')

df_act = df_acticidad.copy()
nombre_barrios = list(set(list(df_acticidad["desc_barrio_local"])))
anyos = list(range(2018,2025))

# Se crea el dataframe
barrios = np.tile(nombre_barrios, len(anyos))
anyo_rep = np.repeat(anyos, len(nombre_barrios))
df_radar = pd.DataFrame({"Barrio": barrios, "anyo": anyo_rep})

# Inicializar columna "Tipo"
df_act["Tipo"] = np.nan


#HOSTELERIA
num_hosteleria = df_acticidad.loc[df_acticidad["actividad_general"] == "HOSTELERIA"]
df_act.loc[df_act["actividad_general"] == "HOSTELERIA", "Tipo"] = "num_hosteleria"

#EDUCACION
num_educacion = df_acticidad.loc[df_acticidad["actividad_general"] == "EDUCACION"]
df_act.loc[df_act["actividad_general"] == "EDUCACION", "Tipo"] = "num_educacion"

#PELUQUERIA Y ESTÉTICA
list_num_peluq_estetica = ["SERVICIO DE PELUQUERIA", "CENTRO DE ESTETICA", "INSTITUTO DE BELLEZA",
                           "CENTROS DE TATUAJE Y/O ANILLADO", "CENTROS DE FOTODEPILACION", "CENTROS DE BRONCEADO",
                           "COMERCIO AL POR MENOR DE ARTICULOS DE PERFUMERIA Y COSMETICA"]
num_peluq_estetica = df_acticidad[df_acticidad['actividad_en_detalle'].isin(list_num_peluq_estetica)]

df_act.loc[df_act['actividad_en_detalle'].isin(list_num_peluq_estetica), "Tipo"] = "num_peluq_estetica"

#SANIDAD
num_sanidad = df_acticidad.loc[df_acticidad["actividad_general"] == "ACTIVIDADES SANITARIAS Y DE SERVICIOS SOCIALES"]
df_act.loc[df_act["actividad_general"] == "ACTIVIDADES SANITARIAS Y DE SERVICIOS SOCIALES", "Tipo"] = "num_sanidad"

#OCIO Y CULTURA
list_num_arte_ocio_cultura = ["ACTIVIDADES DE BIBLIOTECAS, ARCHIVOS, MUSEOS Y DE GALERIAS Y SALAS DE EXPOSICIONES SIN VENTA",
                              "ACTIVIDADES DE CREACION, ARTISTICAS Y ESPECTACULOS", "SALA DE EXPOSICIONES Y GALERIAS DE ARTE CON VENTA",
                              "JUEGOS DE AZAR Y APUESTAS DE GESTION PRIVADA (BINGOS, CASINOS, MAQUINAS TRAGAPERRAS)",
                              "PARQUES ZOOLOGICOS, JARDINES BOTANICOS Y RESERVAS NATURALES"]
num_arte_ocio_cultura = df_acticidad[df_acticidad['actividad_en_detalle'].isin(list_num_arte_ocio_cultura)]
df_act.loc[df_act['actividad_en_detalle'].isin(list_num_arte_ocio_cultura), "Tipo"] = "num_arte_ocio_cultura"


#MODA
list_num_moda = ["COMERCIO AL POR MENOR DE PRENDAS DE VESTIR EN ESTABLECIMIENTOS ESPECIALIZADOS",
                 "CONFECCION PRENDAS DE VESTIR (INCLUIDO CUERO Y EXCLUIDA LA PELETERIA Y LAS PRENDAS DE PUNTO)",
                 "COMERCIO AL POR MENOR DE PRENDAS DE VESTIR EN ESTABLECIMIENTOS ESPECIALIZADOS",
                 "CONFECCION DE PRENDAS DE VESTIR DE PUNTO",
                 "COMERCIO AL POR MENOR DE CALZADO Y ARTICULOS DE CUERO EN ESTABLECIMIENTOS ESPECIALIZADOS"]
num_moda = df_acticidad[df_acticidad['actividad_en_detalle'].isin(list_num_moda)]
df_act.loc[df_act['actividad_en_detalle'].isin(list_num_moda), "Tipo"] = "num_moda"


#ALOJAMIENTOS TURÍSTICOS
list_num_alojamientos = ["CASAS DE HUESPEDES", "ALBERGUES JUVENILES Y OTROS ALOJAMIENTOS TURISTICOS DE CORTA ESTANCIA",
                         "HOSTALES", "PENSIONES", "HOTELES Y MOTELES SIN RESTAURANTE", "VIVIENDAS TURISTICAS",
                         "HOTELES Y MOTELES CON RESTAURANTE", "VIVIENDAS TURISTICA", "PENSIONES",
                         "APART-HOTELES", "CAMPINGS Y APARCAMIENTOS PARA CARAVANAS"]
num_alojamientos = df_acticidad[df_acticidad['actividad_en_detalle'].isin(list_num_alojamientos)]
df_act.loc[df_act['actividad_en_detalle'].isin(list_num_alojamientos), "Tipo"] = "num_alojamientos"


#ACTIVIDADES DE CULTO
num_culto = df_acticidad.loc[(df_acticidad["actividad_en_detalle"] == "ACTIVIDADES DE ORGANIZACIONES RELIGIOSAS")]
df_act.loc[df_act["actividad_en_detalle"] == "ACTIVIDADES DE ORGANIZACIONES RELIGIOSAS", "Tipo"] = "num_culto"


#DEPORTES
list_num_deporte = ["ESTABLECIMIENTOS DE EQUITACION",  "PISCINAS DE USO PUBLLICO CLIMATIZADAS",
                    "PISCINAS DE USO PUBLICO DE TEMPORADA", "ACTIVIDADES DE LOS GIMNASIOS",
                    "ACTIVIDADES DE CLUBES DEPORTIVOS Y OTRAS ACTIVIDADES DEPORTIVAS",
                    "COMERCIO AL POR MENOR DE ARTICULOS DEPORTIVOS"]

num_deporte = df_acticidad[df_acticidad['actividad_en_detalle'].isin(list_num_deporte)]
df_act.loc[df_act['actividad_en_detalle'].isin(list_num_deporte), "Tipo"] = "num_deporte"


#ALIMENTACION               
list_num_alim = ["COMERCIO AL POR MENOR DE PRODUCTOS ALIMENTICIOS NO PERECEDEROS ENVASADOS",
                 "COMERCIO AL POR MAYOR DE HUEVOS Y DERIVADOS",
                 "COMERCIO AL POR MENOR DE PASTELERIA, CONFITERIA, REPOSTERIA SIN OBRADOR",
                 "COMERCIO AL POR MAYOR CARNES Y DERIVADOS, AVES Y CAZA",
                 "COMERCIO AL POR MENOR DE  PASTELERIA, CONFITERIA, REPOSTERIA CON OBRADOR-SIN BARRA DEGUSTACION",
                 "COMERCIO AL POR MENOR DE VINOS Y ALCOHOLES (BODEGA) SIN CONSUMO",
                 "COMERCIO AL POR MENOR DE PESCADOS Y MARISCOS SIN OBRADOR",
                 "COMERCIO AL POR MENOR DE FRUTAS Y HORTALIZAS CON OBRADOR",
                 "COMERCIO AL POR MENOR DE FRUTOS SECOS Y VARIANTES",
                 "COMERCIO AL POR MENOR EN ESTABLECIMIENTOS NO ESPECIALIZADOS, CON PREDOMINIO EN PRODUCTOS ALIMENTICIOS, BEBIDAS Y TABACO (AUTOSERVICIO)",
                 "COMERCIO AL POR MENOR DE LECHE, PRODUCTOS LACTEOS Y BEBIDAS REFRESCANTES",
                 "COMERCIO AL POR MENOR DE PESCADOS Y MARISCOS CON OBRADOR (INCLUYE COCCION)",
                 "COMERCIO AL POR MENOR DE CONGELADOS",
                 "COMERCIO AL POR MENOR CON MAQUINAS EXPENDEDORAS",
                 "COMERCIO AL POR MENOR DE MASAS Y PATATAS FRITAS, CHURRERIA SIN OBRADOR",
                 "COMERCIO AL POR MENOR DE CAFE, INFUSIONES Y CHOCOLATE",
                 "COMERCIO AL POR MENOR DE PAN Y PRODUCTOS DE PANADERIA Y BOLLERIA CON OBRADOR",
                 "COMERCIO AL POR MENOR DE CARNICERIA-SALCHICHERIA",
                 "COMERCIO AL POR MENOR DE CARNICERIA-CHARCUTERIA",
                 "COMERCIO AL POR MENOR DE CARNICERIA",
                 "PUESTO DEL MERCADO CENTRAL DE PESCADOS DE ENVASADO DE PRODUCTOS DE LA PESCA: ENVASADO Y REENVASADO DE PRODUCTOS DE LA PESCA",
                 "COMERCIO AL POR MENOR DE GOLOSINAS"]

num_alim_super  = df_acticidad[df_acticidad['actividad_en_detalle'].isin(list_num_alim)]
df_act.loc[df_act['actividad_en_detalle'].isin(list_num_alim), "Tipo"] = "num_alim_super"


#NEGOCIO TRADICIONAL
list_num_nego_tradi = ["COMERCIO AL POR MENOR DE INSTRUMENTOS MUSICALES",
                       "COMERCIO AL POR MENOR DE LIBROS",
                       "COMERCIO AL POR MENOR DE COLCHONERIA",
                       "LAVADO Y LIMPIEZA DE PRENDAS TEXTILES Y DE PIEL",
                       "VIDEOCLUB",
                       "SERVICIOS DE MENSAJERIA, ACTIVIDADES POSTALES Y DE CORREOS",
                       "ARREGLO DE ROPA",
                       "COMERCIO AL POR MENOR DE SEMILLAS, ABONOS, PLANTAS Y FLOR CORTADA",
                       "COMERCIO AL POR MENOR DE PRODUCTOS DE DROGUERIA",
                       "COMERCIO AL POR MENOR DE JOYAS, RELOJERIA Y BISUTERIA",
                       "FARMACIA",
                       "COMERCIO AL POR MENOR DE ELECTRODOMESTICOS",
                       "COMERCIO AL POR MENOR DE PRODUCTOS DE TELEFONIA Y TELECOMUNICACIONES",
                       "COMERCIO AL POR MENOR DE MATERIAL FOTOGRAFICO Y FOTOGRAFIA",
                       "COMERCIO AL POR MENOR DE APARATOS DE ILUMINACION",
                       "COMERCIO AL POR MENOR DE SANEAMIENTOS",
                       "COMERCIO AL POR MENOR DE MAQUINARIA Y EQUIPOS DE OFICINA",
                       "COMERCIO AL POR MENOR DE MENAJE DEL HOGAR",
                       "COMERCIO AL POR MENOR DE MATERIAL DE OPTICA",
                       "LOCUTORIOS",
                       "COMERCIO AL POR MENOR DE BICICLETAS",
                       "REPARACION DE CALZADO",
                       "COMERCIO AL POR MENOR DE PERIODICOS, REVISTAS Y ARTICULOS DE PAPELERIA",
                       "COMERCIO AL POR MENOR DE TEXTILES PARA EL HOGAR",
                       "IMPRENTA",
                       "COMERCIO AL POR MENOR DE JUEGOS Y JUGUETES",
                       "COMERCIO AL POR MENOR DE ARTICULOS DE FERRETERIA"]

num_nego_tradi  = df_acticidad[df_acticidad['actividad_en_detalle'].isin(list_num_nego_tradi)]
df_act.loc[df_act['actividad_en_detalle'].isin(list_num_nego_tradi), "Tipo"] = "num_nego_tradi"

# Se eliminan las filas con los registros nulos
df_act = df_act.dropna()


list_df = [num_hosteleria, num_educacion, num_peluq_estetica, num_sanidad, num_arte_ocio_cultura, num_moda, num_alojamientos,
           num_culto, num_deporte, num_alim_super, num_nego_tradi]

list_df_col_names = ["num_hosteleria", "num_educacion", "num_peluq_estetica", "num_sanidad", "num_arte_ocio_cultura", "num_moda", "num_alojamientos",
           "num_culto", "num_deporte", "num_alim_super", "num_nego_tradi"]


for dataf in range(len(list_df)):
    for year in anyos:
        dataf_per_year = list_df[dataf].loc[list_df[dataf]["anyo"] == int(year)]
        for barrio_nom in nombre_barrios:
            num_lugar = len(dataf_per_year.loc[dataf_per_year["desc_barrio_local"]==barrio_nom])
            df_radar.loc[(df_radar['anyo'] == int(year)) & (df_radar["Barrio"] == barrio_nom), list_df_col_names[dataf]] = num_lugar

#%%

clean_and_select_places.create_csv(df_radar, 'DATOS/CLEAN/', "flourish_boxplot_act_econ.csv")
clean_and_select_places.create_csv(df_act, 'DATOS/CLEAN/', "actividades_new_category_CARTO.csv")

