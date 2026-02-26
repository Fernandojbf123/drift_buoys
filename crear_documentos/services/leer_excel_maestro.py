import pandas as pd
from crear_documentos.configs.manager_doc_config import *

def leer_excel_maestro(nombre_de_hoja: str = "instalacion", header=None) -> pd.DataFrame:
    """Lee el excel maestro con la información de los despliegues de sondas y devuelve un DataFrame de pandas.

    Descripción:
        Esta función utiliza la ruta al excel maestro y la hoja especificada en la configuración general
        para cargar los datos de los despliegues de sondas. El excel debe contener columnas como "serial",
        "latitud", "longitud", "fecha_de_despliegue", entre otras, que se usarán posteriormente para análisis
        y gráficos.

    Parámetros:
        nombre_de_hoja (str): El nombre de la hoja del excel maestro a leer. Por defecto es "instalacion".
        header (int, None): La fila o filas a usar como encabezado. Por defecto es None, lo que significa que no se usará ningún encabezado.
    Retorna:
        pandas.DataFrame: Un DataFrame con los datos del excel maestro, listo para ser filtrado y analizado."""
        
    ruta = get_ruta_al_excel_maestro()+".xlsx"
    with open(ruta, 'rb') as file:
        df_excel = pd.read_excel(file, sheet_name=nombre_de_hoja, header=header) 
    
    return df_excel
    