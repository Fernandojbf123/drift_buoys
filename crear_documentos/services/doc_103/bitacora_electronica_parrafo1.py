from services.manager_variables_excel_datos_despliegue import *
from services.doc_103.manager_porcentajes import *


def bitacora_electronica_parrafo1(df_datos_despliegue: pd.DataFrame, df_porcentajes: pd.DataFrame) -> str:
    dia_inicio = get_dia_de_liberacion(df_porcentajes = df_porcentajes)
    fecha_final_vigencia = get_fecha_final_vigencia(df_datos_despliegue = df_datos_despliegue)
    numero_de_sondas = get_numero_de_sondas(df_datos_despliegue = df_datos_despliegue)
    
    texto = f'''Respecto a lo anterior, se reportó en el sitio WEB del proyecto el despliegue 
    de {numero_de_sondas} sondas oceanográficas entre el {dia_inicio} y el {fecha_final_vigencia}'''

    return texto