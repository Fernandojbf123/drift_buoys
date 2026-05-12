import pandas as pd
from configs.manager_doc_config import *
from services.leer_excel import leer_excel

def get_df_datos_doris():
    df_datos_doris = leer_excel(get_ruta_al_excel_de_despliegue_de_sondas(), nombre_de_hoja=get_hoja_del_excel_de_despliegue_de_sondas(), header=0)
    return df_datos_doris

def filtrar_df_datos_doris_por_orden_de_servicio(df_datos_doris: pd.DataFrame) -> pd.DataFrame:
    orden_de_servicio = get_orden_de_servicio()
    df_datos_doris.dropna(subset=["OS"], inplace=True) # Elimina filas donde la columna "OS" tenga valores nulos (NaN)
    df_datos_doris["OS"] = df_datos_doris["OS"].astype(int).astype(str).str.strip()
    return df_datos_doris[df_datos_doris["OS"] == orden_de_servicio]

def get_latitudes(df_datos_doris: pd.DataFrame) -> list:
    latitudes = df_datos_doris["latitud_maniobra"].tolist()
    return latitudes
    
def get_longitudes(df_datos_doris: pd.DataFrame) -> list:
    longitudes = df_datos_doris["longitud_maniobra"].tolist()
    return longitudes

def get_fechas_de_despliegue(df_datos_doris: pd.DataFrame) -> list:
    fechas_de_despliegue = df_datos_doris["fecha_maniobra"].tolist()
    return fechas_de_despliegue