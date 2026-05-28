from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *
from services.doc_103.manager_porcentajes import *
import pandas as pd

def bitacora_electronica_parrafo1(df_datos_campanias: pd.DataFrame, df_datos_despliegue: pd.DataFrame, df_porcentaje: pd.DataFrame) -> str:
    fecha_inicio_vigencia = get_fecha_inicio_vigencia_texto(df_datos_despliegue = df_datos_despliegue)
    mes_y_anio_de_liberacion = get_mes_y_anio_de_liberacion(df_datos_campanias = df_datos_campanias)
    
    texto = f'''Respecto a lo anterior, se reportó en el sitio WEB del proyecto el despliegue 
    de siete sondas oceanográficas entre el {fecha_inicio_vigencia} y el {mes_y_anio_de_liberacion}'''

    return texto