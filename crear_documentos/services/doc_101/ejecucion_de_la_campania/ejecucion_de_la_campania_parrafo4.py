
from configs.manager_doc_config import *

from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *

from services.timestamp_a_texto_espanol import *
from services.obtener_palabras_singulares_plurales import *


def ejecucion_de_la_campania_parrafo4(df_datos_campanias: pd.DataFrame) -> str:

    df_unicos = get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_campanias=df_datos_campanias)

    if len(df_unicos) <= 1:
        return "A continuación,"

    return (
        "Dado que las actividades asociadas a la ejecución de las campañas "
        "para la liberación de sondas oceanográficas son similares entre ellas, "
        "a continuación,"
    )