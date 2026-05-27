import pandas as pd
from configs.manager_doc_config import *
from services.leer_excel import leer_excel
from services.timestamp_a_texto_espanol import *

## DATOS ASOCIADOS AL EXCEL DE PORCENTAJES
def get_df_porcentajes():
    df_porcentajes = leer_excel(get_ruta_al_excel_de_porcentajes(), nombre_de_hoja= "Sheet1", header=0)
    return df_porcentajes

def get_porcentaje_maximo_de_transmision(df_porcentajes: pd.DataFrame) -> str:
    porcentaje_maximo_de_transmision = df_porcentajes["porcentaje_de_transmision"].max()
    return f"{porcentaje_maximo_de_transmision:.2f}%"       
