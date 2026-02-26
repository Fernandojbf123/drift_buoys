import os
import pandas as pd
from ..utils.utils_get_doc_config import get_ruta_a_carpeta_de_las_figuras

def crear_diccionario_del_df_excel_maestro(df: pd.DataFrame) -> dict:
    """Crea un diccionario a partir de un DataFrame del excel maestro.

    Descripción:
        Esta función toma un DataFrame que contiene los datos del excel maestro
        y crea un diccionario donde las claves son los nombres de las columnas
        y los valores son listas con los datos correspondientes.

    Parámetros:
        df (pandas.DataFrame): El DataFrame del excel maestro.

    Retorna:
        dict: Un diccionario con los datos del DataFrame."""
    
    output_dict = {}
    
    var_names = df.iloc[:,0]
    for var_name in var_names:
        idx = df[df.iloc[:,0] == var_name].index
        
        if var_name == "seriales_elegidos":
            var_values = df.iloc[idx, 1:].dropna(axis=1).values.flatten().tolist()
            var_values = [str(int(value)) for value in var_values]
            
        if var_name == "conclusiones":
             var_values = df.iloc[idx, 1:].replace({pd.NA: ""}).values.flatten().tolist()[0:6]
             
        if "fig" in var_name:
            var_values = df.iloc[idx, 1:].dropna(axis=1).values.flatten().tolist()
            carpeta = get_ruta_a_carpeta_de_las_figuras()
            var_values = [os.path.join(carpeta, str(value)+".png") for value in var_values]
        else:
            var_values = df.iloc[idx, 1:].dropna(axis=1).values.flatten().tolist()
        
        output_dict[var_name] = var_values
        
    return output_dict

