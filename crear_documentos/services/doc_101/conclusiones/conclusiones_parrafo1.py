from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *

def conclusiones_parrafo1(dic_datos_doris: dict) -> str:
    
    numero_total_de_sondas = get_numero_total_de_sondas()
    
    texto = f"Se desplegaron exitosamente {numero_total_de_sondas} sondas oceanográficas en las localizaciones solicitadas por PEMEX."
    
    return texto