from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *


def bitacora_electronica_parrafo1(df_datos_campanias: pd.DataFrame, df_datos_despliegue: pd.DataFrame) -> str:
    
    df_unicos= get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_campanias = df_datos_campanias)
    fechas_campanias_unicos = df_unicos["fecha_hora_de_embarque"].tolist()
    campanias_unicos = df_unicos["campania"].tolist()
    mes_y_anio_de_liberacion = get_mes_y_anio_de_liberacion(df_datos_campanias = df_datos_campanias)
    
    texto = f'''Respecto a lo anterior, se reportó en el sitio WEB del proyecto el despliegue 
    de siete sondas oceanográficas entre el {fechas_campanias_unicos[0]} y el {fechas_campanias_unicos[-1]} de {mes_y_anio_de_liberacion}'''

    return texto