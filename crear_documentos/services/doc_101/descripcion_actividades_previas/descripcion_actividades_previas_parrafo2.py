from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *

def descripcion_actividades_previas_parrafo2(df_datos_campanias: pd.DataFrame, df_datos_despliegue: pd.DataFrame) -> str:
    
    df_unicos = get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_campanias = df_datos_campanias)
    numero_de_sondas = get_numero_de_sondas(df_datos_despliegue = df_datos_despliegue)
    
    es_una_campania = len(df_unicos) == 1
    articulo = "la" if es_una_campania else "las"
    palabra_campania = "campaña" if es_una_campania else "campañas"
    
    texto = f"Las actividades previas a {articulo} {palabra_campania} de liberación, comenzaron una vez que PEMEX proporcionó"
    texto += f" al personal de ASM-CICESE las coordenadas para el despliegue de las {numero_de_sondas} sondas oceanográficas,"
    texto += f" diseñadas conforme a las necesidades específicas de PEMEX. Previo al despliegue de las sondas se realizaron las"
    texto += f" actividades determinadas de acuerdo al plan de trabajo del personal y, en la medida de lo posible, se consideraron"
    texto += f" los tiempos programados en el Plan de Campaña de cada despliegue. "
    
    return texto