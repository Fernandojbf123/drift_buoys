import pandas as pd
from configs.manager_doc_config import *
from services.leer_excel import leer_excel
from services.timestamp_a_texto_espanol import *

## DATOS ASOCIADOS AL EXCEL DE PORCENTAJES
def get_df_porcentajes():
    df_porcentajes = leer_excel(get_ruta_al_excel_de_porcentajes(), nombre_de_hoja= "Sheet1", header=0)
    return df_porcentajes

def get_porcentaje_maximo_de_transmision(df_porcentajes: pd.DataFrame) -> str:
    porcentaje_maximo_de_transmision = df_porcentajes["porcentaje_de_datos_recibidos_mas_interpolados"].max()
    return f"{porcentaje_maximo_de_transmision:.2f}%"       
           
def get_periodo_de_transmision(df_porcentajes: pd.DataFrame) -> str:

    df_porcentajes["fecha_inicio"] = pd.to_datetime(df_porcentajes["fecha_de_inicio"], format="%d-%m-%Y %H:%M:%S", errors="coerce")
    df_porcentajes["fecha_final"] = pd.to_datetime(df_porcentajes["fecha_de_finalizacion"], format="%d-%m-%Y %H:%M:%S", errors="coerce")

    periodos = []
    for _, row in df_porcentajes.iterrows():

        inicio = row["fecha_inicio"].strftime("%d/%m/%Y")
        fin = row["fecha_final"].strftime("%d/%m/%Y")

        periodos.append(f"del {inicio} al {fin}")

    return " y ".join(periodos)