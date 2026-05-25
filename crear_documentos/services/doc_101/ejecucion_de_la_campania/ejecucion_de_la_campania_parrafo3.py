from configs.manager_doc_config import *

from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *

from services.timestamp_a_texto_espanol import *
from services.obtener_palabras_singulares_plurales import *

def ejecucion_de_la_campania_parrafo3(df_datos_campanias: pd.DataFrame, df_datos_despliegue: pd.DataFrame) -> str:
    
    df_unicos= get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_campanias = df_datos_campanias)
    fechas_campanias_unicos = df_unicos["fecha_hora_de_embarque"].tolist()
    campanias_unicos = df_unicos["campania"].tolist()
    
    es_una_campania = True if len(df_unicos) == 1 else False
    p = obtener_palabras_singulares_plurales(es_singular = es_una_campania)
   
    texto = ""
    for i, (fecha_campania, campania) in enumerate(zip(fechas_campanias_unicos, campanias_unicos)):
        
        if i == 0:
            texto += f"{campania} realizada el {timestamp_a_texto_espanol(fecha_campania, mes_y_anio = False)}"
        
        elif i < len(fechas_campanias_unicos) - 1:
            texto += f", la campaña {campania} realizada el {timestamp_a_texto_espanol(fecha_campania, mes_y_anio = False)}"       
        
        elif i == len(fechas_campanias_unicos) - 1:
            texto += f" y la campaña {campania} realizada el {timestamp_a_texto_espanol(fecha_campania, mes_y_anio = False)}"
            
    return texto
