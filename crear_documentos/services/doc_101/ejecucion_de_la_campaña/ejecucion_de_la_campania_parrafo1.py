from configs.manager_doc_config import *
from services.manager_variables_excel_datos_doris import *


def ejecucion_de_la_campania_parrafo1(dic_datos_doris: dict) -> str:
    
    numero_total_de_sondas = get_numero_total_de_sondas()
    mes_campania = get_mes_campania()
    anio_campania = get_anio_campania()
    dia_campania1 = get_dia_campania1()
    dia_camapania2 = get_dia_campania2()
    
    texto = f"La logística para la preparación y despliegue de las sondas fue planeada y enviada con antelación a PEMEX para su aprobación. El derrotero o ruta de liberación de las sondas consideró el trayecto desde tierra hasta el lugar de despliegue de las {numero_total_de_sondas} sondas oceanográficas el {dia_campania1} y el {dia_camapania2} de {mes_campania} de {anio_campania}, tomando en cuenta las condiciones ambientales y la posición."
    
    return texto