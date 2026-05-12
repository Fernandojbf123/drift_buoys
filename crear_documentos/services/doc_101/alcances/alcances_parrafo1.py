from configs.manager_doc_config import *
from services.manager_variables_excel_datos_doris import *

def alcances_parrafo1(dic_datos_doris: dict) -> str:
    
    orden_de_servicio = get_orden_de_servicio()
    
    texto = f'''Con base en las especificaciones particulares del Contrato No. 658225821,
    en este documento se reportan las actividades asociadas al concepto “10.1
    Protocolo de liberación de las sondas oceanográficas y transmisión de datos”,
    relacionadas con las sondas oceanográficas liberadas en abril de 2026,
    las cuales se ejecutaron para dar cumplimiento a la orden de servicio
    PEMEX-ASM-CICESE-658225821-{orden_de_servicio} e incluyen los siguientes alcances:'''
    
    return texto
