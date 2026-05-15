
from configs.manager_doc_config import *
from crear_documentos.services.manager_variables_excel_datos_despliegue import *

def ejecucion_de_la_campania_parrafo3(dic_datos_doris: dict) -> str:
    
    numero_total_de_sondas = get_numero_total_de_sondas()
    texto = f"El despliegue de las sondas se dio de manera exitosa en las {numero_total_de_sondas} sondas desplegadas; todas las sondas funcionaron perfectamente durante y después del despliegue."
    
    return texto