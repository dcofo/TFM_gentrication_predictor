# -*- coding: utf-8 -*-
"""
ARCHIVO AUXILIAR

@author: nievesfo
"""

import pandas as pd

# Cargar el archivo CSV original
df = pd.read_csv("DATOS/CLEAN/general_data_v3.csv")

# Definir las columnas que se mantendrán
id_vars = ['Barrio', 'anyo', 'anyo_timestamp']

# Las demás columnas serán transformadas
value_vars = [col for col in df.columns if col not in id_vars]

# Aplicar la transformación al formato largo
df_melted = df.melt(id_vars=id_vars, value_vars=value_vars,
                    var_name='Indicador', value_name='valor_indicador')

# Guardar el nuevo DataFrame en un archivo CSV
df_melted.to_csv("DATOS/CLEAN/general_data_transformado_CARTO2.csv", index=False)

print("Archivo transformado guardado como 'general_data_transformado_CARTO2.csv'")

