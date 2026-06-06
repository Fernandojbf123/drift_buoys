import pandas as pd
from configs.manager_doc_config import *
from services.leer_excel import leer_excel
from services.timestamp_a_texto_espanol import *

## DATOS ASOCIADOS A LA HOJA DE CAMPAÑAS
def get_df_datos_campanias():
    df_datos_campanias = leer_excel(get_ruta_al_excel_de_campanias(), nombre_de_hoja=get_hoja_del_excel_de_campanias(), header=0)
    return df_datos_campanias

def filtrar_datos_de_campanias(df_datos_campanias: pd.DataFrame, seriales_de_sondas: list[str]) -> pd.DataFrame:
    df_datos_campanias.dropna(subset=["serial_boya"], inplace=True) # Elimina filas donde la columna "serial_boya" tenga valores nulos (NaN)
    df_datos_campanias["serial_boya"] = df_datos_campanias["serial_boya"].astype(str).str.strip()
    df_datos_campanias = df_datos_campanias[df_datos_campanias["serial_boya"].isin(seriales_de_sondas)]
    return df_datos_campanias


# DE LOS DATOS DE LAS MANIOBRAS Y DEL EMBARQUE
def get_fecha_y_hora_de_maniobra(df_datos_campanias: pd.DataFrame) -> list[pd.Timestamp]:
    fechas_de_maniobra = pd.to_datetime(df_datos_campanias["fecha_y_hora_de_maniobra"], format= "%d/%m/%Y %H:%M", errors='coerce')
    fechas_de_maniobra = fechas_de_maniobra.tolist()
    return fechas_de_maniobra

def get_lat_maniobra(df_datos_campanias: pd.DataFrame) -> list[float]:
    latitudes = df_datos_campanias["lat_maniobra"].tolist()
    return latitudes
    
def get_lon_maniobra(df_datos_campanias: pd.DataFrame) -> list[float]:
    longitudes = df_datos_campanias["lon_maniobra"].tolist()
    return longitudes

def get_fecha_hora_de_embarque(df_datos_campanias: pd.DataFrame) -> list[pd.Timestamp]:
    fecha_hora_de_embarque = pd.to_datetime(df_datos_campanias["fecha_hora_de_embarque"], format= "%d/%m/%Y %H:%M", errors='coerce')
    fecha_hora_de_embarque = fecha_hora_de_embarque.tolist()
    return fecha_hora_de_embarque


# DE LA PLANIFICACIÓN DEL CRUCERO
def get_campania(df_datos_campanias: pd.DataFrame) -> list[str]:
    campania = df_datos_campanias["campania"].tolist()
    return campania

def get_fecha_y_hora_de_plan(df_datos_campanias: pd.DataFrame) -> list[pd.Timestamp]:
    fecha_y_hora_de_plan = pd.to_datetime(df_datos_campanias["fecha_y_hora_de_plan"], format= "%d/%m/%Y %H:%M", errors='coerce')
    fecha_y_hora_de_plan = fecha_y_hora_de_plan.tolist()
    return fecha_y_hora_de_plan

def get_lat_plan(df_datos_campanias: pd.DataFrame) -> list[float]:
    latitud_plan = df_datos_campanias["lat_plan"].tolist()
    return latitud_plan

def get_lon_plan(df_datos_campanias: pd.DataFrame) -> list[float]:
    longitud_plan = df_datos_campanias["lon_plan"].tolist()
    return longitud_plan


def get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_campanias: pd.DataFrame) -> pd.DataFrame:
    df_output = df_datos_campanias[["fecha_hora_de_embarque", "campania"]].drop_duplicates()
    return df_output

def get_mes_y_anio_de_liberacion(df_datos_campanias: pd.DataFrame) -> str:
    df = get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_campanias)
    df["fecha_hora_de_embarque"] = pd.to_datetime(df["fecha_hora_de_embarque"], format= "%d/%m/%Y %H:%M", errors='coerce')
    mes_y_anio_de_liberacion = df["fecha_hora_de_embarque"].iloc[0]
    mes_y_anio_de_liberacion = timestamp_a_texto_espanol(mes_y_anio_de_liberacion, mes_y_anio=True) 
    return mes_y_anio_de_liberacion

def get_fecha_y_hora_sonda_individual(df_datos_despliegue: pd.DataFrame):
    fechas_horas = pd.to_datetime(
        df_datos_despliegue["fecha_y_hora_de_despliegue_campo"],
        format="%d/%m/%Y %H:%M",
        errors="coerce")
    fecha = fechas_horas.dt.strftime("%d/%m/%Y").tolist()
    hora = fechas_horas.dt.strftime("%H:%M").tolist()

    return fecha, hora