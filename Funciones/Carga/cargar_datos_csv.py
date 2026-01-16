# Imports generales
import pandas as pd
import numpy as np
import os
import copy
from dotenv import load_dotenv

################### NO TOCAR #########################
# Utilidades
from Funciones.Correctores.corrector_utils import *
from Funciones.Utils.utilidades import *
# Carga asociadas a las configuraciones y a las variables
from Funciones.Utils.utils_get_config_vars import *
from Funciones.Utils.utils_get_vars_dic import *

#################### FUNCIONES #########################

def buscar_nombre_de_archivo_de_sonda():
    """A partir de la lista se seriales de las sondas indicadas en el archivo de configuración,
    se generan las rutas a cada archivo CSV correspondiente de la sonda.
    Retorna:
        rutas_de_sondas: lista de rutas completas a los archivos CSV de las sondas encontradas -> lista de strings
        seriales_encontrados: lista de seriales de sondas para las que se encontraron archivos CSV -> lista de strings
    """
    carpeta_de_datos_crudos = crear_ruta_a_carpeta(get_carpeta_datos_crudos())
    archivos_en_carpeta = os.listdir(carpeta_de_datos_crudos)

    seriales_de_sondas = get_seriales_sondas()
    if not archivos_en_carpeta:
        raise FileNotFoundError(f"No se encontraron archivos en la carpeta: {carpeta_de_datos_crudos}") 
    if not seriales_de_sondas:
        raise ValueError("La lista de seriales de sondas está vacía.")  

    archivos_csv = []
    for archivo in archivos_en_carpeta:
        if archivo.endswith('.csv'):
            archivos_csv.append(archivo)
    
    rutas_de_sondas = []
    seriales_encontrados = []
    for serial_de_sonda in seriales_de_sondas:
        for archivo in archivos_csv:
            if serial_de_sonda in archivo:
                rutas_de_sondas.append(os.path.join(carpeta_de_datos_crudos,archivo))
                seriales_encontrados.append(serial_de_sonda)


    for serial_de_sonda in seriales_de_sondas:
        if serial_de_sonda not in seriales_encontrados:
            print(f"La sonda {serial_de_sonda} no tiene un archivo CSV en la carpeta de datos crudos.")

    return rutas_de_sondas, seriales_encontrados

def cargar_datos_de_sonda(rutas_de_sondas: list, seriales_de_sondas: list)-> dict:
    """ Esta función se encarga de cargar los datos de cada archivos CSV de cada sonda
    a partir de las rutas a los archivos CSV y de los seriales de sondas encontrados por la función 'buscar_nombre_de_archivo_de_sonda'.
    La salida es un diccionario cuyos keys son los seriales de las sondas y los valores son los dataframes son los dataframes crudos de cada sonda.
    Cada dataframe tiene los nombres de columnas estandarizadas y la columna de fechas 'tspan_de_envio' en formato pd.datetime.
    """
    
    output_dir = {}

    for iserial, serial in enumerate(seriales_de_sondas):
        ruta_de_sonda = rutas_de_sondas[iserial] # Ruta completa al archivo CSV de la sonda
        try:
            output_dir[serial] = pd.read_csv(ruta_de_sonda)
            
            # Buscar los nombres de columnas de los datos crudos
            nombres_columnas_crudos = output_dir[serial].columns.tolist()
            nombres_de_columnas_estandarizados = obtener_nombres_estandarizados(nombres_columnas_crudos)

            # Asignar nombres de columnas esperados
            output_dir[serial].columns = nombres_de_columnas_estandarizados # Asignar nombres de columnas
            
            # Cambiar el formato de datos de tspan a pandas datetime
            output_dir[serial] = cambiar_fechas_a_pd_datetime(output_dir[serial], serial)
            print(f"Datos cargados correctamente para la sonda: {serial}")
        except FileNotFoundError:
            print(f"Archivo no encontrado: {ruta_de_sonda}")
        except pd.errors.EmptyDataError:
            print(f"El archivo está vacío: {ruta_de_sonda}")
        except Exception as e:
            print(f"Ocurrió un error al cargar los datos de la sonda {ruta_de_sonda}: {e}")

    return output_dir


def leer_excel_de_despliegue_de_sondas(seriales_encontrados: list) -> pd.DataFrame:
    """ Lee el archivo Excel que contiene la información de despliegue de las sondas y devuelve un dataframe con datos de despliegue de las sondas 
    para las que se encontraron datos.

    Estructura del DataFrame de salida :
        serie_de_sonda = string
        fecha_y_hora_de_despliegue = pd.datetime
        fecha_y_hora_de_la_primera_transmision = pd.datetime
        latitud_de_despliegue = float
        longitud_de_despliegue = float
        campania = string
    """
    ruta_al_excel_de_despliegue_de_sondas = crear_ruta_a_carpeta(get_ruta_al_excel_de_despliegue_de_sondas())   
    ruta_al_excel_de_despliegue_de_sondas = ruta_al_excel_de_despliegue_de_sondas + ".xlsx"
    try:

        df_excel = pd.read_excel(ruta_al_excel_de_despliegue_de_sondas)
        df_excel = df_excel[df_excel['serie_de_sonda'].notna()]

        df_excel['serie_de_sonda'] = df_excel['serie_de_sonda'].astype(int).astype(str)
        
        df_excel['fecha_y_hora_de_despliegue'] = pd.to_datetime(df_excel['fecha_y_hora_de_despliegue'], format="%d/%m/%Y %H:%M")
        df_excel['fecha_y_hora_de_la_primera_transmision'] = pd.to_datetime(df_excel['fecha_y_hora_de_la_primera_transmision'], format="%d/%m/%Y %H:%M")
        df_excel['fecha_y_hora_de_ultima_transmision'] = pd.to_datetime(df_excel['fecha_y_hora_de_ultima_transmision'], format="%d/%m/%Y %H:%M")
        df_excel['latitud_de_despliegue'] = df_excel['latitud_de_despliegue'].str.split(' ').str[0].astype(float)
        df_excel['longitud_de_despliegue'] = df_excel['longitud_de_despliegue'].str.split(' ').str[0].astype(float)
        df_excel['campania'] = df_excel['campania']
     
        # Encontrar sondas sin datos
        sondas_sin_datos = df_excel[df_excel['fecha_y_hora_de_la_primera_transmision'].isna()]['serie_de_sonda'].tolist()

        # Avisarle a usuario qué sondas no tienen datos y que serán excluidas del analisis
        seriales_de_sondas = get_seriales_sondas()
        for serial in seriales_de_sondas:
            if serial not in seriales_encontrados or serial in sondas_sin_datos:
                print(f"La sonda {serial} no tiene datos cargados y será excluida del análisis.")   

        df_excel = df_excel[df_excel["serie_de_sonda"].isin(seriales_encontrados)].reset_index(drop=True)
        
        return df_excel
    
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo Excel en la ruta: {ruta_al_excel_de_despliegue_de_sondas}")
    except Exception as e:
        raise ValueError(f"Ocurrió un error al leer el archivo Excel: {e}")


def seleccionar_rango_de_fechas(diccionario: dict, df_excel_de_despliegue: pd.DataFrame, seriales_encontrados: list)-> dict:
    """ Recibe el diccionario con los dataframe de cada serial cargado. 
    Filtra los datos para que solo queden los que están dentro del rango de fechas especificado en la configuración general.

    seriales_encontrados: lista de seriales de sondas para las que se encontraron archivos CSV -> lista de strings
    df_excel_de_despliegue: DataFrame con la información de despliegue de las sondas.
    diccionario: diccionario con los dataframes de cada sonda cargados.

    Retorna un diccionario con los dataframes filtrados por rango de fechas.
    """
    fecha_de_inicio_del_analisis = get_fecha_de_inicio_del_analisis() # de configuraciones
    fecha_de_fin_del_analisis = get_fecha_de_fin_del_analisis() # de configuraciones
    
    output_dic = copy.deepcopy(diccionario)
    for serial in seriales_encontrados:
        
        fecha_de_primera_medicion = df_excel_de_despliegue[df_excel_de_despliegue["serie_de_sonda"]==serial]["fecha_y_hora_de_la_primera_transmision"].values[0] # del excel de despliegue
        fecha_de_la_ultima_medicion = diccionario[serial]["tspan_de_envio"].max() # de los datos cargados
        
        fecha_de_inicio = max(fecha_de_inicio_del_analisis, fecha_de_primera_medicion) # fecha de inicio es la menor entre la fecha de inicio del análisis y la fecha de la primera medición
        fecha_de_fin = min(fecha_de_fin_del_analisis, fecha_de_la_ultima_medicion) # fecha de fin es la mayor entre la fecha de fin del análisis y la fecha de la última medición

        df = output_dic[serial]
        mask = (df["tspan_de_envio"] >= fecha_de_inicio) & (df["tspan_de_envio"] <= fecha_de_fin)
        output_dic[serial] = df.loc[mask].reset_index(drop=True)

    return output_dic

def buscar_y_eliminar_duplicados(diccionario: dict, seriales_encontrados: list)-> dict:
    """ Busca y elimina los datos duplicados en cada dataframe del diccionario dado.
    seriales_encontrados: lista de seriales de sondas para las que se encontraron archivos CSV -> lista de strings
    Retorna un diccionario con los dataframes sin datos duplicados.
    """
    
    for serial in seriales_encontrados: # los keys del diccionario son el número de serie de cada sonda
        df = diccionario[serial] # DataFrame de la sonda antes del filtrado
        duplicados_explicitos = buscar_duplicados_explicitos(data = df)
        diccionario[serial] = eliminar_datos_duplicados(data = df, duplicados_explicitos = duplicados_explicitos, serie_de_sonda = serial)
    
    return diccionario


def ordernar_datos_por_fecha(diccionario: dict, seriales_encontrados: list) -> dict:
    """ Ordena los datos de cada dataframe del diccionario por la columna de fechas 'tspan_de_envio'.
    seriales_encontrados: lista de seriales de sondas para las que se encontraron archivos CSV -> lista de strings
    """
    for serial in seriales_encontrados:
        df = diccionario[serial]
        diccionario[serial] = ordenar_df_por_fecha(data = df,serial_de_sonda=serial)
    return diccionario

def crear_tspan_redondeado(diccionario: dict, seriales_encontrados: list)->dict:
    """ recibe el diccionario que contiene los dataframe de cada sonda y modifica el tspan de cada dataframe.
    seriales_encontrados: lista de seriales de sondas para las que se encontraron archivos CSV -> lista de strings
    
    Regla de redondeo:
    Si HH:MM es < 30 mins se redondea a HH:00
    Si HH:MM es >=30 y <=59 se redondea a HH:30"""

    for serial in seriales_encontrados:
        df = diccionario[serial]
        tspan_mod = [tspan_value.replace(minute=0) if tspan_value.minute < 30 else tspan_value.replace(minute=30) for tspan_value in df["tspan_de_envio"]]
        df["tspan_rounded"] = tspan_mod
        diccionario[serial] = df
    
    return diccionario

def existen_fechas_redondeadas_duplicadas(diccionario: dict, seriales_encontrados: list) -> bool:
    """ Verifica si existen fechas redondeadas duplicadas en los dataframes del diccionario.
    seriales_encontrados: lista de seriales de sondas para las que se encontraron archivos CSV -> lista de strings
    """
    for serial in seriales_encontrados:
        df = diccionario[serial]
        duplicados = df["tspan_rounded"].value_counts()
        duplicados_implicitos = duplicados[duplicados > 1]
        if not duplicados_implicitos.empty:
            print(duplicados_implicitos)
            raise ValueError(f"Se encontraron {duplicados_implicitos.sum()} fechas redondeadas duplicadas en la sonda {serial}. Deteniendo ejecución")
    return print("No se encontraron fechas redondeadas duplicadas en ninguna sonda.")

def get_cols_names_sin_tspan(diccionario: dict) -> list:
    """ Devuelve una lista con los nombres de las columnas del dataframe dado, excluyendo las columnas de fechas 'tspan_de_envio' y 'tspan_rounded'.
    """
    seriales = list(diccionario.keys())
    data = diccionario[seriales[0]] # tomar el dataframe de la primera sonda. 
    columnas = list(data.columns)
    columnas.remove("tspan_de_envio")
    columnas.remove("tspan_rounded")
    return columnas

def crear_diccionario_con_dataframes_vacios(diccionario: dict, keys: list) -> dict:
    """ Crea un diccionario cuyos keys son los seriales de las sondas; y dentro de cada key se encontra un dataframe vacío 
    con las fechas sintéticas generadas y con las columnas dadas en keys.
    keys: lista de nombres de columnas que debe tener cada dataframe vacío (excluyendo tspan_de_envio y tspan_rounded)
    """
    delta_tiempo = get_delta_tiempo()
    
    output_dic = {}
    for serial in diccionario.keys():
        df = diccionario[serial]
        fecha_de_primera_medicion = df["tspan_de_envio"].min()
        fecha_de_ultima_medicion = df["tspan_de_envio"].max()

        fecha_de_inicio = fecha_de_primera_medicion.replace(minute=0) if fecha_de_primera_medicion.minute < 30 else fecha_de_primera_medicion.replace(minute=30) # redondear la fecha inicial
        fecha_de_fin = fecha_de_ultima_medicion.replace(minute=0) if fecha_de_ultima_medicion.minute < 30 else fecha_de_ultima_medicion.replace(minute=30) # redondear la fecha final
        tspan_sintetico = crear_rango_de_fechas_sintetico(fecha_de_inicio, fecha_de_fin, delta_tiempo)
        
        output_dic[serial] = {}
        
        diccionario_de_apoyo = {
            "tspan":tspan_sintetico
        }

        data = diccionario[serial] # dataframe de la sonda original
        # Bucle para crear columnas vacías según el tipo de dato del dataframe original
        for key in keys:
            if pd.api.types.is_numeric_dtype(data[key]): # Si es numérico
                diccionario_de_apoyo[key]= np.full(len(tspan_sintetico), np.nan)
            elif pd.api.types.is_string_dtype(data[key]): # Si es string
                diccionario_de_apoyo[key]= np.full(len(tspan_sintetico), "")

        df = pd.DataFrame(diccionario_de_apoyo) # Crear DataFrame vacío con las fechas sintéticas y columnas vacías
        output_dic[serial] = df # Asignar el DataFrame vacío al diccionario de salida
    
    return output_dic

def merge_df_vacio_con_datos(diccionario_con_datos: dict, diccionario_con_dfs_vacios: dict) -> dict:
    """Para cada sonda se buscan el diccionario de datos y el diccionario de dataframes vacíos, luego se combinan ambos dataframe.
    El dataframe con datos tiene tspan_de_envio y tspan_rounded, mientras que el dataframe vacío solo tiene tspan; que es una columna de fechas
    sintéticas redondeadas desde el despliegue de la sonda hasta el fin del periodo de análisis.
    El resultado es un nuevo diccionario con un dataframe para cada sonda, donde cada dataframe tiene todas las fechas posibles 
    en donde deben haber datos entre el inicio y fin del análisis. Si en una fecha hay datos, se mantienen esos datos, si no tiene datos,
    se coloca NaN o "" según el tipo de dato de la columna."""

    output_dic = {}
    seriales = list(diccionario_con_datos.keys())

    for serial in seriales:
        df_vacio = diccionario_con_dfs_vacios[serial].set_index("tspan") # Buscar el dataframe vacío de la sonda y asignar tspan como índice
        df_sonda = diccionario_con_datos[serial].set_index("tspan_rounded") # Buscar el dataframe con datos de la sonda y asignar tspan_rounded como índice
        df_sonda.rename(columns={"tspan":"tspan_de_envio"}, inplace=True)  # Cambiar el nombre de la columna tspan para evitar conflictos
        # combine_first mantiene todas las fechas de df_vacio y pone NaN donde no hay datos en df_sonda
        df_merged = df_vacio.combine_first(df_sonda)
        df_merged.index.name = "tspan_rounded"
        output_dic[serial] = df_merged.reset_index()

    return output_dic

def agregar_componentes_de_la_velocidad(diccionario: dict) -> dict:
    """ Agrega las columnas de velocidad u y v al dataframe de cada sonda en el diccionario."""
    seriales = list(diccionario.keys())
    for serial in seriales:
        df = diccionario[serial]
        # Convertir direccion de grados a radianes
        dir = df["dir_corriente"]
        rap = df["rap_corriente"]
        [u,v] = polar2uv(dir, rap)
        # Calcular componentes u y v
        df["u_corriente"] = u
        df["v_corriente"] = v
        diccionario[serial] = df    

    return diccionario