from configs.manager_doc_config import *
from crear_documentos.services.manager_variables_excel_datos_campania import *
from services.manager_variables_excel_datos_despliegue import *
import datetime

def ejecucion_de_la_campania_parrafo1(dic_datos_doris: dict) -> str:
    
    numero_total_de_sondas = get_numero_de_sondas(dic_datos_doris)
    fecha_campania = get_fecha_y_hora_de_embarque_y_campania_unicos(dic_datos_doris)
    fecha = datetime.strptime(fecha_campania.iloc[0], "%Y-%m-%d %H:%M:%S")
    fecha_campania_fin = datetime.strptime(fecha_campania.iloc[1], "%Y-%m-%d %H:%M:%S")
    dia_campania_inicio = fecha.day 
    dia_campania_fin = fecha_campania_fin.iloc[-1].day
    mes_campania = fecha.month
    anio_campania = fecha.year
    articulo = "la" if len(fecha_campania) == 1 else "las"
    palabra_campania = "campaña" if len(fecha_campania) == 1 else "campañas"
    instalaciones = {dia_campania_inicio} if len(fecha_campania) == 1 else f"{dia_campania_inicio} y el {dia_campania_fin}"
    
    if len(fecha_campania_fin) == 3:
        fecha_campania_fin = datetime.strptime(fecha_campania.iloc[-1], "%Y-%m-%d %H:%M:%S")
        dia_campania_fin = fecha_campania_fin.day
         
    texto = f"La logística para la preparación y despliegue de las sondas fue planeada y enviada con antelación a PEMEX para su aprobación. El derrotero o ruta de liberación de las sondas consideró el trayecto desde tierra hasta el lugar de despliegue de las {numero_total_de_sondas} sondas oceanográficas el {instalaciones} de {mes_campania} de {anio_campania}, tomando en cuenta las condiciones ambientales y la posición. De acuerdo a lo anterior, la ejecución de {articulo} {palabra_campania} de liberación siguió un procedimiento seguro en todas las actividades que involucran la travesía y las maniobras del despliegue. "
    
    return texto