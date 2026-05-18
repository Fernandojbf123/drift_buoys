from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *


def ejecucion_de_la_campania_parrafo4(dic_datos_doris: dict) -> str:
    dos_despliegues= get_fecha_y_hora_de_embarque_y_campania_unicos(dic_datos_doris)
    
    if len(dos_despliegues) == 1:
        return (
            f"La Figura {dos_despliegues[0]} "
            "muestra las localizaciones solicitadas."
        )

    numeros = " y ".join(map(str, dos_despliegues))

    return (
        f"Las Figuras {numeros} "
        "muestran las localizaciones solicitadas."
    )