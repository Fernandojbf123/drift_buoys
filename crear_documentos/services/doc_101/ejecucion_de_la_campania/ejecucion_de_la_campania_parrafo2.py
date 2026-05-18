from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from crear_documentos.services.manager_variables_excel_datos_campania import *


def ejecucion_de_la_campania_parrafo2(dic_datos_doris: dict) -> str:
    
    df_unicos= get_fecha_y_hora_de_embarque_y_campania_unicos(dic_datos_doris)
    
    texto = "Dado que las actividades asociadas a la ejecución de "
    articulo = "la" if len(df_unicos) == 1 else "las"
    palabra_campania = "campaña" if len(df_unicos) == 1 else "campañas"
    texto = f"La ejecución de {articulo} {palabra_campania} de instalación de las sondas, se efectuó de acuerdo con la planeación de la logística y derrotero de la embarcación."
        
    return texto

