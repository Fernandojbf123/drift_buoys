from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from crear_documentos.services.manager_variables_excel_datos_campania import *
import datetime

def descripcion_actividades_previas_parrafo3(dic_datos_doris: dict) -> str:
    df_unicos = get_fecha_y_hora_de_embarque_y_campania_unicos(dic_datos_doris)
    orden_de_servicio = get_orden_de_servicio()
    numero_total_de_sondas = get_numero_de_sondas(dic_datos_doris)
    
    es_una_campania = len(df_unicos) == 1
    articulo = "la" if es_una_campania else "las"
    palabra_campania = "campaña" if es_una_campania else "campañas"
    palabra_embarcacion = "embarcación" if es_una_campania else "embarcaciones"
    cual = "cual" if es_una_campania else "cuales"
    envio = "fue" if es_una_campania else "fueron"
    este = "este" if es_una_campania else "estos"
    
    texto = f"Posteriormente, para {articulo} {palabra_campania}, se planeó la logística de {articulo} {palabra_embarcacion} en {articulo} {cual} se transportaron las sondas al lugar del despliegue. La liberación de las {numero_total_de_sondas} sondas se llevo a cabo el {fecha_campania}. La ruta de liberación de las sondas en {articulo} {palabra_campania}, obedeció el trayecto óptimo considerando la distancia desde tierra hasta el lugar de liberación acordado con PEMEX, teniendo en cuenta las condiciones atmosféricas y las posiciones en las cuales se hicieron las liberaciones. El derrotero consideró el sitio donde se dispuso del equipo que se utilizó para la liberación de las sondas y los implementos adicionales que se utilizaron para las maniobras costa afuera. Es importante mencionar que el derrotero de {articulo} {palabra_embarcacion} está sujeto a cambios de acuerdo a las condiciones atmosféricas el día del zarpe, y a las decisiones que el encargado de la embarcación considere mejor para salvaguardar la seguridad de toda la tripulación. Una vez realizado el plan de crucero de {articulo} {palabra_campania} (ver ANEXO 3: PLAN DE CRUCERO), {este} {envio} enviados a PEMEX para su autorización, previo a la ejecución de {articulo} {palabra_embarcacion}, y de acuerdo con lo acordado en el Contrato No. 658225821. "
  
    return texto







