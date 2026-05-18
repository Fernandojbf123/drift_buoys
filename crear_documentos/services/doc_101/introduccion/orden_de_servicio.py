from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *

def orden_de_servicio(dic_datos_doris: dict) -> str:
         
    orden_de_servicio = get_orden_de_servicio()
    
    
    texto = f"{orden_de_servicio}."
        
    return texto

