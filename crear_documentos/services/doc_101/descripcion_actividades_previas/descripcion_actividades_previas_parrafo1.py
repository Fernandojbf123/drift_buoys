from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *

def descripcion_actividades_previas_parrafo1(dic_datos_doris: dict) -> str:
    df_unicos= get_fecha_y_hora_de_embarque_y_campania_unicos(dic_datos_doris)
    orden_de_servicio = get_orden_de_servicio()
    numero_total_de_sondas = get_numero_de_sondas(dic_datos_doris)

    es_una_campania = len(df_unicos) == 1
    articulo = "la" if es_una_campania else "las"
    palabra_campania = "campaña" if es_una_campania else "campañas"
    if len(df_unicos) == 1:
        texto = f"Las actividades previas a {articulo} {palabra_campania} de despliegue de las {numero_total_de_sondas} sondas oceanográficas, realizadas por el consorcio All Solutions de México S. A. de C. V. (ASM) y el Centro de Investigación Científica y Educación Superior de Ensenada (CICESE), y para dar cumplimiento a lo establecido en la sección 10.1 del Contrato No. 658225821 “Protocolo de liberación de las sondas oceanográficas y transmisión de datos”, relacionadas con la Orden de Servicio PEMEX-ASM-CICESE-658225821-{orden_de_servicio} se presentan a continuación."
   
    return texto