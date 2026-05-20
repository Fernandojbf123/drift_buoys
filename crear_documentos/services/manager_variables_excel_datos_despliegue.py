import pandas as pd
from configs.manager_doc_config import *
from services.leer_excel import leer_excel


## Datos asociados a la hoja de datos de DORIS
def get_df_datos_despliegue():
    df_datos_despliegue = leer_excel(get_ruta_al_excel_de_despliegue_de_sondas(), nombre_de_hoja=get_hoja_del_excel_de_despliegue_de_sondas(), header=0)
    return df_datos_despliegue

def filtrar_df_datos_despliegue_por_orden_de_servicio(df_datos_despliegue: pd.DataFrame) -> pd.DataFrame:
    orden_de_servicio = get_orden_de_servicio()
    df_datos_despliegue.dropna(subset=["OS"], inplace=True) # Elimina filas donde la columna "OS" tenga valores nulos (NaN)
    df_datos_despliegue["OS"] = df_datos_despliegue["OS"].astype(int).astype(str).str.strip()
    return df_datos_despliegue[df_datos_despliegue["OS"] == orden_de_servicio]

def get_seriales_de_sondas(df_datos_despliegue: pd.DataFrame) -> list[str]:
    seriales_de_sondas = df_datos_despliegue["serial_de_sonda"].astype(str).str.strip().tolist()
    return seriales_de_sondas

def get_numero_de_sondas(df_datos_despliegue: pd.DataFrame) -> int:
    numero_de_sondas = len(df_datos_despliegue)
    return numero_de_sondas

def get_fecha_inicio_de_vigencia(df_datos_despliegue: pd.DataFrame) -> str:
    fecha_inicio_de_vigencia = df_datos_despliegue["fecha_inicio_de_vigencia"].iloc[0]
    fecha_inicio_de_vigencia = pd.to_datetime(fecha_inicio_de_vigencia, format= "%d/%m/%Y", errors='coerce')
    fecha_inicio_de_vigencia = fecha_inicio_de_vigencia.strftime("%d de %B de %Y")
    return fecha_inicio_de_vigencia

def get_fecha_final_de_vigencia(df_datos_despliegue: pd.DataFrame) -> str:
    fecha_inicio_de_vigencia = df_datos_despliegue["fecha_inicio_de_vigencia"].iloc[0]
    fecha_inicio_de_vigencia = pd.to_datetime(fecha_inicio_de_vigencia, format= "%d/%m/%Y", errors='coerce')
    fecha_final_de_vigencia = fecha_inicio_de_vigencia + pd.offsets.MonthEnd(0)
    fecha_final_de_vigencia = fecha_final_de_vigencia.strftime("%d de %B de %Y")
    return fecha_final_de_vigencia

def get_fecha_de_entrega(df_datos_despliegue: pd.DataFrame) -> str:
    fecha_de_inicio_de_vigencia = df_datos_despliegue["fecha_inicio_de_vigencia"].iloc[0]
    fecha_inicio_de_vigencia = pd.to_datetime(fecha_de_inicio_de_vigencia, format= "%d/%m/%Y", errors='coerce')
    fecha_de_entrega = fecha_inicio_de_vigencia + pd.DateOffset(months=1)
    fecha_de_entrega = fecha_de_entrega.strftime("%d de %B de %Y")
    return fecha_de_entrega



