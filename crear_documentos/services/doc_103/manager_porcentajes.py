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
    return f"{porcentaje_maximo_de_transmision:.2f}"       

def get_periodo_de_transmision(df_porcentajes: pd.DataFrame) -> str:
    df = df_porcentajes.copy() 
    df["fecha_inicio"] = pd.to_datetime(df["fecha_de_inicio"], format="%d-%m-%Y %H:%M:%S", errors="coerce").dt.date
    df["fecha_final"] = pd.to_datetime(df["fecha_final"], format="%d-%m-%Y %H:%M:%S", errors="coerce").dt.date
    df["fecha_final"] = df["fecha_final"].fillna(df["fecha_inicio"])
    periodos_df = (df[["fecha_inicio", "fecha_final"]].dropna(subset=["fecha_inicio"]).drop_duplicates().sort_values("fecha_inicio"))

    periodos = []
    for _, row in periodos_df.iterrows():
        inicio = row["fecha_inicio"].strftime("%d/%m/%Y")
        fin = row["fecha_final"].strftime("%d/%m/%Y")
        if row["fecha_inicio"] == row["fecha_final"]:
            periodos.append(f"el {inicio}")
        else:
            periodos.append(f"del {inicio} al {fin}")

    if not periodos:
        return ""
    if len(periodos) == 1:
        return periodos[0]
    if len(periodos) == 2:
        return " y ".join(periodos)
    return ", ".join(periodos[:-1]) + " y " + periodos[-1]

def get_dia_de_liberacion(df_porcentajes: pd.DataFrame) -> str: 
    df_porcentajes["fecha_de_inicio"] = pd.to_datetime(
    df_porcentajes["fecha_de_inicio"], format="%d/%m/%Y %H:%M", errors="coerce") 
    fecha_primera = df_porcentajes["fecha_de_inicio"].iloc[0]
    dia = fecha_primera.day
    return dia

def get_periodo_transmision_sonda_individual(df_porcentajes: pd.DataFrame, serial_de_sonda: str) -> str:

    df_filtrado = df_porcentajes[df_porcentajes["serial_de_sonda"].astype(str).str.strip() == str(serial_de_sonda).strip()].copy()
    if df_filtrado.empty:
        return ""
    df_filtrado["fecha_de_inicio"] = pd.to_datetime(df_filtrado["fecha_de_inicio"], format="%d/%m/%Y %H:%M", errors="coerce")
    df_filtrado["fecha_final"] = pd.to_datetime(df_filtrado["fecha_final"], format="%d/%m/%Y %H:%M", errors="coerce")
    fecha_inicio = df_filtrado["fecha_de_inicio"].min()
    fecha_final = df_filtrado["fecha_final"].max()
    fecha_inicio = fecha_inicio.strftime("%d/%m/%Y")
    fecha_final = fecha_final.strftime("%d/%m/%Y")
    
    return f"del {fecha_inicio} al {fecha_final}"