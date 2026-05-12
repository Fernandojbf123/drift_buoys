from configs.manager_doc_config import *
from services.manager_variables_excel_datos_doris import *

def intro_parrafo1(dic_datos_doris: dict) -> str:
         
    orden_de_servicio = get_orden_de_servicio()
    
    
    texto = f'''Este reporte describe y enumera las actividades realizadas por el consorcio All Solutions de México S. A. de C. V. 
    (en lo sucesivo ASM) y el Centro de Investigación Científica y Educación Superior de Ensenada (en lo sucesivo CICESE) para la preparación, 
    movilización y finalmente el     despliegue satisfactorio de sondas oceanográficas; dando cumplimiento así 
    al compromiso establecido en la sección 10.1 del contrato No. 658225821 “Reporte del protocolo de liberación de las sondas oceanográficas y 
    transmisión de datos.” y específicamente a la Orden de Servicio 
    PEMEX-ASM-CICESE-658225821-{orden_de_servicio}.'''
        
    return texto

