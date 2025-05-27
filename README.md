# TFM_gentrication_predictor
En este repositorio se almacena el código desarrollado para el proyecto "Factores y predicción de la gentrificación en la ciudad de Madrid" englobado dentro del trabajo final del Máster de Ciencia de Datos de la Universitat Oberta de Catalunya (UOC).

En este archivo se resumen: la estructura creada y los pasos a seguir para la ejecución de cada uno de los scripts, en caso de querer replicar los resultados.

# Cómo se estructura el código
Todos los scripts se encuentran en el directorio principal junto a unos scripts auxiliares que se han usado para modificar la estructura de los archivos de datos finales de cara a su representación gráfica en las distintas plataformas usadas en el proyecto: CARTO y Flourish. Para ejecutar el código se facilita el archivo de requerimientos con las librerías necesarias. Una vez instalado ya es posible empezar a ejecutar los scripts para transformar los archivos originales ( alojados dentro del directorio 'DATOS'**). A continuación, se deja la lista del orden llevado a cabo para ello:

1. Archivo de transformación de actividades económicas -->  script clean_and_select_places.py
2. Archivo de inversiones -->  script inversiones.py
3. Archivo de airbnb's -->  script airbnb.py
4. Archivo de indicadores por barrio --> script indicadores_per_barrio.py
5. Archivos que amplían el número de indicadores --> script complete_indicador_file.py
6. Aplicación del algoritmo de machine learning: script kmeans.py

OPCIONAL:
7. Los scripts AUX_CARTO_cambio_estru.py y AUX_flourish.py sirven para modificar la estructura de los archivos CSV resultantes para su representación en las distintas plataformas online de visualización de datos.

** Es necesario tener en cuenta, en caso de querer replicar los pasos del proyecto, que hay algunos archivos de datos que se encuentran comprimidos debido diversos problemas encontrados para subir archivos de más de 100MB al repositorio. Los intentos por solucionarlo no han dado sus frutos por lo que se ha optado por subir los archivos comprimidos.


