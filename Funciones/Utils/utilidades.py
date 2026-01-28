import os
import numpy as np
import pandas as pd
import pickle
from dotenv import load_dotenv
import netCDF4 as nc

from matplotlib.figure import Figure

from Funciones.Utils.utils_get_vars_dic import *
from Funciones.Utils.utils_get_config_vars import *
################### NO TOCAR #########################

###################### FUNCIONES ######################

##################### A #########################

##################### B #########################

##################### C #########################

def calcular_porcentaje_de_datos_recibidos(diccionario: dict) -> dict:
    """ Calcula el porcentaje de datos recibidos en un DataFrame."""
    cantidad_de_datos_esperados = []
    cantidad_de_datos_recibidos = []
    porcentajes = []

    seriales_de_sondas = list(diccionario.keys()) 

    for iserial, serial in enumerate(seriales_de_sondas):
        data = diccionario[serial]
        cantidad_de_datos_esperados.append(len(data))
        cantidad_de_datos_recibidos.append(data.dropna().shape[0])
        porcentaje = 0

        if cantidad_de_datos_esperados != 0:
            porcentaje = round((cantidad_de_datos_recibidos[iserial] / cantidad_de_datos_esperados[iserial]) * 100, 2)

        porcentajes.append(porcentaje)


    dic = {
        "serial_de_sonda": seriales_de_sondas,
        "cantidad_de_datos_esperados": cantidad_de_datos_esperados,
        "cantidad_de_datos_recibidos": cantidad_de_datos_recibidos,
        "porcentaje_de_datos_recibidos": porcentajes
    }
        
    dataout = pd.DataFrame(dic)
    return dataout

#######################
def calcular_porcentaje_de_datos_interpolados(diccionario: dict, tabla_de_porcentajes) -> dict:
    
    seriales_de_sondas = list(diccionario.keys())
    for iserial, serial in enumerate(seriales_de_sondas):
        data = diccionario[serial]
        var_names = get_variables_graficar()
        cantidad_de_datos_esperados = tabla_de_porcentajes["cantidad_de_datos_esperados"][iserial]
        cantidad_de_datos_recibidos = tabla_de_porcentajes["cantidad_de_datos_recibidos"][iserial]
        cantidad_de_Datos_despues_de_interpolar = data[var_names[0]].dropna().value_counts().sum()
        cantidad_de_datos_interpolados = cantidad_de_Datos_despues_de_interpolar - cantidad_de_datos_recibidos
        
        porcentaje_recibidos_e_interpolados = 0
        if cantidad_de_datos_interpolados != 0:
            porcentaje_recibidos_e_interpolados = round((cantidad_de_Datos_despues_de_interpolar / cantidad_de_datos_esperados) * 100, 2)
        
        tabla_de_porcentajes.loc[tabla_de_porcentajes["serial_de_sonda"] == serial, "cantidad_de_datos_interpolados"] = cantidad_de_datos_interpolados
        tabla_de_porcentajes.loc[tabla_de_porcentajes["serial_de_sonda"] == serial, "cantidad_de_datos_recibidos_mas_interpolados"] = cantidad_de_Datos_despues_de_interpolar
        tabla_de_porcentajes.loc[tabla_de_porcentajes["serial_de_sonda"] == serial, "porcentaje_de_datos_recibidos_mas_interpolados"] = porcentaje_recibidos_e_interpolados

    return tabla_de_porcentajes
#######################

def cambiar_fechas_a_pd_datetime(df: pd.DataFrame, serial:str) -> pd.DataFrame:
    """ Cambia el formato de las fechas en la columna especificada de un DataFrame a datetime."""
    
    columna_fecha = "tspan_de_envio"  # Nombre de la columna que contiene las fechas
 
    try:
        df[columna_fecha] = pd.to_datetime(df[columna_fecha], format="%Y-%m-%dT%H:%M:%S.000Z")
    except Exception as e:
        print(f"Ocurrió un error al cambiar el formato de las fechas para la sonda {serial}: {e}")
    
    return df
#######################

def cargar_datos_de_batimetria() -> dict:
    """ Carga datos de batimetría desde un archivo NetCDF. Especificada en el archivo de configuración general.
    Salida
    
    datos_batimetria = {
        "lon": array_like,
        "lat": array_like,
        "elevation": array_like,
        "curvas_de_batimetria": array_like
    }
    
    """
    datos_batimetria = {
        "lon": None,
        "lat": None,
        "elevation": None,
        "curvas_de_batimetria": get_curvas_de_batimetria()
    }
    
    ruta = get_ruta_a_datos_batimetria()
        
    with nc.Dataset(ruta) as data:
        lon = data.variables['lon'][:]
        lat = data.variables['lat'][:]
        elevation = data.variables['elevation'][:,:]

        LON, LAT = np.meshgrid(lon, lat)   
    
        datos_batimetria["lon"] = LON
        datos_batimetria["lat"] = LAT
        datos_batimetria["elevation"] = elevation
    
    return datos_batimetria
#######################

def cargar_diccionario_pickle(ruta_archivo):
    """
    Carga un diccionario desde un archivo pickle.

    Parámetros:
    ruta_archivo (str): Ruta del archivo pickle.

    Retorna:
    dict: Diccionario cargado desde el archivo.
    """

    ruta_archivo = ruta_archivo+".pkl"
    
    if not os.path.isfile(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
    
    with open(ruta_archivo, 'rb') as file:
        diccionario = pickle.load(file)
    
    return diccionario
#####################

def crear_rango_de_fechas_sintetico(fecha_de_inicio: pd.Timestamp, fecha_de_fin: pd.Timestamp, delta_tiempo: str) -> pd.DatetimeIndex:
    tspan_sintetico = pd.date_range(start=fecha_de_inicio, end=fecha_de_fin, freq=delta_tiempo)
    return tspan_sintetico

#####################

def crear_ruta_a_carpeta(carpeta: str) -> str:
    """ Crea la ruta completa a una carpeta utilizando la variable de entorno 'ruta_al_NAS' si está disponible.
    carpeta: Ruta relativa a la carpeta deseada."""
    load_dotenv() # Cargar variables de entorno desde el archivo .env
    ruta_al_NAS = os.getenv("ruta_al_NAS")    
    ruta_completa = carpeta
    if ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)        
    
    return ruta_completa

#####################

##################### G #########################
def guardar_diccionario_como_pickle(diccionario: dict, ruta: str,nombre_archivo: str) -> None:
    """
    Entrada:
    diccionario (dict): Diccionario con los datos a guardar.
    ruta_completa (str): Ruta completa con nombre de archivo donde se guardará el archivo pickle.
    eg. /carpeta/subcarpeta/nombre_archivo.pickle
    Salida:
    None
    """
    if not os.path.exists(ruta):
        os.makedirs(ruta)

    with open(os.path.join(ruta,nombre_archivo+".pkl"), 'wb') as handle:
        pickle.dump(diccionario, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Diccionario guardado correctamente en {os.path.join(ruta,nombre_archivo+'.pkl')}")

#####################
def guardar_figura(figura: Figure, ruta_a_carpeta: str, nombre_archivo: str, formato: str = "png", resolucion: int = 300) -> None:
    """
    Guarda una figura en la ruta especificada con el formato y resolución dados.

    Parámetros:
    figura (Figure): Objeto de la figura a guardar.
    ruta_a_carpeta (str): Ruta a la carpeta donde se guardará la figura.
    nombre_archivo (str): Nombre del archivo sin extensión.
    formato (str): Formato de la figura ('png', 'jpg', 'svg', 'pdf').
    resolucion (int): Resolución en dpi.

    Retorna:
    None
    """
    try:
        if not os.path.exists(ruta_a_carpeta):
            os.makedirs(ruta_a_carpeta)

        ruta_completa = os.path.join(ruta_a_carpeta, f"{nombre_archivo}.{formato}")
        figura.savefig(ruta_completa, format=formato, dpi=resolucion, bbox_inches='tight')
        print(f"Figura guardada correctamente en {ruta_completa}")
        
    except Exception as e:
        print(f"Ocurrió un error al guardar la figura: {e}")
    
#####################

def guardar_porcentajes_en_excel(data: pd.DataFrame, ruta: str, nombre_de_archivo: str) -> None:
    
    try:
        if not os.path.exists(ruta):
            os.makedirs(ruta)

        ruta_completa = os.path.join(ruta, nombre_de_archivo+".xlsx")
        data.to_excel(ruta_completa, index=False)
        print(f"Archivo Excel guardado correctamente en {ruta_completa}")
    except Exception as e:
        print(f"Ocurrió un error al guardar el archivo Excel: {e}")

#####################

##################### O #########################

##################### P #########################

def polar2uv(dir_deg, spd):
    # Convertir grados a radianes
    dir_rad = np.radians(dir_deg)
    # Componente este (u)
    u = spd * np.sin(dir_rad)
    # Componente norte (v)
    v = spd * np.cos(dir_rad)
    return u, v

#####################

##################### U #########################
def uv2polar(u, v):
    # Magnitud
    spd = np.hypot(u, v)
    # Dirección en radianes (como MATLAB: cart2pol(v, u))
    dir_rad = np.arctan2(u, v)
    # Ajuste de ángulo negativo
    dir_rad = np.where(dir_rad < 0, dir_rad + 2 * np.pi, dir_rad)
    # Convertir a grados
    dir_deg = np.degrees(dir_rad)
    return dir_deg, spd

#####################