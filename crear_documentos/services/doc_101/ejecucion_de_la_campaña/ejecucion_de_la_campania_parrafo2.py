from configs.manager_doc_config import *
from services.manager_variables_excel_datos_doris import *


def ejecucion_de_la_campania_parrafo2(dic_datos_doris: dict) -> str:
    
    asm= get_asm()
    fecha_campania = get_fecha_campania()
    
    texto = f"Dado que las actividades asociadas a la ejecución de las campañas ({asm1} y {asm2}) es similar en ambos casos, a continuación, se describe la ejecución de la campaña {asm1} realizada el {fecha_campania1}."
    
    return texto