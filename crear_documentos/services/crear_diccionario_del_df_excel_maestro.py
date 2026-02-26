import os
import pandas as pd
from ..configs.manager_doc_config import get_ruta_a_carpeta_de_las_figuras

def aux_crear_datos_para_tabla_2():
    return None

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
            output_dict[f"<<{var_name}>>"] = var_values
            
        elif var_name == "conclusiones":
             var_values = df.iloc[idx, 1:].replace({pd.NA: ""}).values.flatten().tolist()[0:6]
             output_dict[f"<<{var_name}>>"] = var_values
             
        elif "fig" in var_name: # Este va de la mano con "pie" linea 49
            memoria_de_var_name = var_name
            output_dict[f"<<{var_name}>>"] = []
            
            tmp_dic = {
                "ruta": None,
                "titulo": None,
                "tamanio": 6 #inches para el word
            }
            
            var_values = df.iloc[idx, 1:].dropna(axis=1).values.flatten().tolist()
            carpeta = get_ruta_a_carpeta_de_las_figuras()
            for value in var_values:
                ruta = os.path.join(carpeta, str(value)+".png")
                tmp_dic["ruta"] = ruta
                output_dict[f"<<{var_name}>>"].append(tmp_dic.copy())
                
        elif "pie" in var_name: # Este va de la mano con "fig" linea 32
            var_values = df.iloc[idx, 1:].replace({pd.NA: ""}).values.flatten().tolist()
            for i, _ in enumerate(output_dict[f"<<{memoria_de_var_name}>>"]):
                output_dict[f"<<{memoria_de_var_name}>>"][i]["titulo"] = var_values[i]
            
            
        else:
            var_values = df.iloc[idx, 1:].dropna(axis=1).values.flatten().tolist()
            output_dict[f"<<{var_name}>>"] = var_values
        
    return output_dict

