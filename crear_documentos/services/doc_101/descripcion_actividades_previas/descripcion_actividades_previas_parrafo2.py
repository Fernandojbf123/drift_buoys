from configs.manager_doc_config import *
from crear_documentos.services.manager_variables_excel_datos_despliegue import *


def descripcion_actividades_previas_parrafo2(dic_datos_doris: dict) -> str:
    
    
    orden_de_servicio = get_orden_de_servicio()
    numero_total_de_sondas = get_numero_total_de_sondas()
    numero_de_sondas_campania1 = get_numero_de_sondas_campana1()
    numero_de_sondas_campania2 = get_numero_de_sondas_campana2()
    fecha_campania_1 = get_fecha_campania_1()
    fecha_campania_2 = get_fecha_campania_2()
    
    if fecha_campania_2 == "N/A":   
        texto = f"Posteriormente, para cada campaña, se planeó la logística de las embarcaciones en la cuales se transportaron las sondas al lugar del despliegue. La liberación de las {numero_total_de_sondas} se llevo a cabo el {fecha_campania_1}. La ruta de liberación de las sondas en ambas campañas, obedeció el trayecto óptimo considerando la distancia desde tierra hasta el lugar de liberación acordado con PEMEX, teniendo en cuenta las condiciones atmosféricas y las posiciones en las cuales se hicieron las liberaciones. El derrotero consideró el sitio donde se dispuso del equipo que se utilizó para la liberación de las sondas y los implementos adicionales que se utilizaron para las maniobras costa afuera. Es importante mencionar que el derrotero de las embarcaciones está sujeto a cambios de acuerdo a las condiciones atmosféricas el día del zarpe, y a las decisiones que el encargado de la embarcación considere mejor para salvaguardar la seguridad de toda la tripulación. Una vez realizado el plan de crucero de cada campaña (ver ANEXO 3: PLAN DE CRUCERO), estos fueron enviados a PEMEX para su autorización, previo a la ejecución de las campañas, y de acuerdo con lo acordado en el Contrato No. 658225821. "
    else:
        texto = f"Posteriormente, para cada campaña, se planeó la logística de las embarcaciones en la cuales se transportaron las sondas al lugar del despliegue. Cabe mencionar que la liberación de las {numero_total_de_sondas} sondas se dividió en dos campañas; {numero_de_sondas_campania_1} sondas se liberaron el {fecha_campania_1}, y {numero_de_sondas_campania_2} más el {fecha_campania_2}. La ruta de liberación de las sondas en ambas campañas, obedeció el trayecto óptimo considerando la distancia desde tierra hasta el lugar de liberación acordado con PEMEX, teniendo en cuenta las condiciones atmosféricas y las posiciones en las cuales se hicieron las liberaciones. El derrotero consideró el sitio donde se dispuso del equipo que se utilizó para la liberación de las sondas y los implementos adicionales que se utilizaron para las maniobras costa afuera. Es importante mencionar que el derrotero de las embarcaciones está sujeto a cambios de acuerdo a las condiciones atmosféricas el día del zarpe, y a las decisiones que el encargado de la embarcación considere mejor para salvaguardar la seguridad de toda la tripulación. Una vez realizado el plan de crucero de cada campaña (ver ANEXO 3: PLAN DE CRUCERO), estos fueron enviados a PEMEX para su autorización, previo a la ejecución de las campañas, y de acuerdo con lo acordado en el Contrato No. 658225821."
    
    return texto