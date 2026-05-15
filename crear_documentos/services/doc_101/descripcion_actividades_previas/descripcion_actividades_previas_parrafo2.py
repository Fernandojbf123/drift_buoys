from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *
    
    
def descripcion_actividades_previas_parrafo2(dic_datos_doris: dict) -> str:
    df_unicos= get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_de_campanias)
    
    if len(df_unicos) == 1:
        numero_de_sondas = get_numero_de_sondas(df_datos_doris)
        
        texto = f"Las actividades previas a la campaña de liberación, comenzaron una vez que PEMEX proporcionó al personal de ASM-CICESE las coordenadas para el despliegue de las {numero_de_sondas} sondas oceanográficas, diseñadas conforme a las necesidades específicas de PEMEX. Previo al despliegue de las sondas se realizaron las actividades determinadas de acuerdo al plan de trabajo del personal y, en la medida de lo posible, se consideraron los tiempos programados en el Plan de Campaña de cada despliegue. "
    else:
        texto = f"Las actividades previas a las campañas de liberación, comenzaron una vez que PEMEX proporcionó al personal de ASM-CICESE las coordenadas para el despliegue de las {numero_de_sondas} sondas oceanográficas, diseñadas conforme a las necesidades específicas de PEMEX. Previo al despliegue de las sondas se realizaron las actividades determinadas de acuerdo al plan de trabajo del personal y, en la medida de lo posible, se consideraron los tiempos programados en el Plan de Campaña de cada despliegue. "
    
    return texto 