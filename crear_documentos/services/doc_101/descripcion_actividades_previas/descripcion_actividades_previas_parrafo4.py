from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *

from services.manager_variables_excel_datos_campania import *

def descripcion_actividades_previas_parrafo4(dic_datos_doris: dict) -> str:
    
    numero_total_de_sondas = len(get_fecha_hora_de_embarque(dic_datos_doris))
    mes_campania = get_fecha_y_hora_de_embarque_y_campania_unicos(dic_datos_doris).strftime("%B")
    mes_orden_de_servicio = get_orden_de_servicio().split()[3]
    
    texto = f"De esta forma, se realizaron las pruebas de funcionamiento en las {numero_total_de_sondas} sondas que se desplegaron, correspondientes a la orden de servicio del mes de {mes_orden_de_servicio}."
    
    return texto