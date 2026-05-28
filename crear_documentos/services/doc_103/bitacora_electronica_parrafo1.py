from configs.manager_doc_config import *
from services.manager_variables_excel_datos_campania import *
from services.doc_103.manager_porcentajes import *
import pandas as pd

def bitacora_electronica_parrafo1(df_datos_campanias: pd.DataFrame, df_porcentajes: pd.DataFrame) -> str:
    dia_inicio = get_dia_de_liberacion(df_porcentajes = df_porcentajes)
    mes_y_anio_de_liberacion = get_mes_y_anio_de_liberacion(df_datos_campanias = df_datos_campanias)
    
    texto = f'''Respecto a lo anterior, se reportó en el sitio WEB del proyecto el despliegue 
    de siete sondas oceanográficas entre el {dia_inicio} y el {mes_y_anio_de_liberacion}'''

    return texto