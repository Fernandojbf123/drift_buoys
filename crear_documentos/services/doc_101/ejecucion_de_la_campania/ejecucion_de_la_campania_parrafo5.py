from configs.manager_doc_config import *

from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *

from services.timestamp_a_texto_espanol import *
from services.obtener_palabras_singulares_plurales import *

def ejecucion_de_la_campania_parrafo5(df_datos_campanias: pd.DataFrame, df_datos_despliegue: pd.DataFrame) -> str:
    
    numero_de_sondas = get_numero_de_sondas(df_datos_despliegue = df_datos_despliegue)
    
    texto = f"El despliegue de las sondas se dio de manera exitosa en las {numero_de_sondas}"
    
    return texto