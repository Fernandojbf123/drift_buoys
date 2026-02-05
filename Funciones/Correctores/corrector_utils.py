import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.dates as mdates  

from Funciones.Utils.utilidades import uv2polar
from Funciones.Utils.utils_get_config_vars import *
from Funciones.Utils.utils_get_vars_dic import *
############### # FUNCIONES DE CORRECCIÓN DE DATOS ###############

################# B #################
def buscar_duplicados_explicitos(data: pd.DataFrame) -> pd.DataFrame:
    """ Crea un dataframe que tiene filas únicas y cuantas veces se repite cada fila.
    Retorna el dataframe con los datos duplicados
    """
    duplicados = data.value_counts()
    duplicados_explicitos = duplicados[duplicados > 1]
    return duplicados_explicitos

################# E #################
def eliminar_datos_duplicados(data: pd.DataFrame, duplicados_explicitos, serie_de_sonda) -> pd.DataFrame:
    """ Elimina los datos duplicados en los dataframes del diccionario dado."""
    if duplicados_explicitos.sum() > 0: # Si hay duplicados
        print(f"Se encontraron {duplicados_explicitos.sum()} datos duplicados en la sonda {serie_de_sonda}. Eliminándolos...")  
        data.drop_duplicates(inplace=True)

    return data.reset_index(drop=True)


################################

def eliminar_datos_espurios(diccionario: dict) -> dict:
    """ Busca filas donde la rapidez sea mayor a 2 m/s y reemplaza todos los valores 
    de esa fila con NaN, excepto las columnas tspan_rounded y tspan_de_envio."""
    seriales_de_sondas = list(diccionario.keys())
    if not diccionario:
        return diccionario  # Retorna el diccionario vacío si no hay datos
    
    for serial in seriales_de_sondas:
        df = diccionario[serial].copy()
        # Crear máscara para identificar filas con rapidez > 2
        mask = df["rap_corriente"] > 2
        
        # Obtener todas las columnas excepto tspan_rounded y tspan_de_envio
        columnas_a_reemplazar = [col for col in df.columns if col not in ["tspan_rounded", "tspan_de_envio"]]
        
        # Reemplazar valores con NaN en las filas que cumplen la condición
        df.loc[mask, columnas_a_reemplazar] = np.nan
        
        diccionario[serial] = df
        
        # Imprimir información sobre los datos espurios encontrados
        if mask.sum() > 0:
            print(f"Sonda {serial}: Se encontraron {mask.sum()} filas con rapidez > 2 m/s. Valores reemplazados con NaN.")
    
    return diccionario
################################


################# I #################
def interpolar_datos_faltantes(diccionario: dict) -> dict:
    """ Interpola los datos faltantes en los dataframes del diccionario dado."""
    seriales_de_sondas = list(diccionario.keys())
    output_dic = {}

    try:
        for serial_de_sonda in seriales_de_sondas:
            
            tspan_completo = diccionario[serial_de_sonda]["tspan_rounded"] # prueba para evitar error de variable no usada
            tspan_numeric_completo = mdates.date2num(tspan_completo)

            data = diccionario[serial_de_sonda]
            new_data = data.dropna().reset_index(drop=True)
            tspan_numeric_real = mdates.date2num(new_data["tspan_rounded"])

            for column in data.columns:
                if pd.api.types.is_numeric_dtype(data[column]) and "tspan" not in column and column != "rap_corriente" and column != "dir_corriente":
                    # obtener función de interpolación
                    f = interp1d(tspan_numeric_real, new_data[column], kind='linear', fill_value=np.nan, bounds_error=False)
                    # interpolar en las fechas completas
                    data[column] = f(tspan_numeric_completo)
            
            # Ahora se corrige rap_corriente y dir_corriente por separado (La rap y dir se deben calcular apartir de las componentes u y v)
            data["dir_corriente"], data["rap_corriente"] = uv2polar(data["u_corriente"], data["v_corriente"])

            # guardo el dataframe con los datos interpolados
            output_dic[serial_de_sonda] = data
            
    except Exception as e:
         raise ValueError(f"Ocurrió un error al interpolar los datos: {e}")

    return output_dic

################# O #################
def ordenar_df_por_fecha(data: pd.DataFrame, serial_de_sonda: str) -> pd.DataFrame:
    """ Ordena los datos de cada dataframe del diccionario por la columna de fechas 'tspan'."""
    try:
        data = data.sort_values(by="tspan_de_envio").reset_index(drop=True)
        print(f"Datos ordenados por fecha para la sonda {serial_de_sonda}.")
        return data
    except Exception as e:
         raise ValueError(f"Ocurrió un error al ordenar los datos por fecha: {e}")