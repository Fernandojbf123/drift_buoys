from configs.manager_doc_config import *
from services.manager_variables_excel_datos_campania import *
from services.manager_variables_excel_datos_despliegue import *

from services.obtener_palabras_singulares_plurales import *

def ejecucion_de_la_campania_parrafo1(df_datos_campanias: pd.DataFrame, df_datos_despliegue: pd.DataFrame) -> str:
    
    df_unicos = get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_campanias = df_datos_campanias)
    es_una_campania = True if len(df_unicos) == 1 else False
    
    p = obtener_palabras_singulares_plurales(es_singular = es_una_campania)
    
    texto = f"De acuerdo a lo anterior, la ejecución de {p["la_las"]} {p["campania_campanias"]} de liberación siguió un"
    texto += " procedimiento seguro en todas las actividades que involucran la travesía y las maniobras del despliegue"
    
    return texto