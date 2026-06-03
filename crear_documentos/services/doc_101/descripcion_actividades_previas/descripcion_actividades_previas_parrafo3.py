from configs.manager_doc_config import *

from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *

from services.timestamp_a_texto_espanol import *
from services.obtener_palabras_singulares_plurales import *


def descripcion_actividades_previas_parrafo3(df_datos_campanias: pd.DataFrame, df_datos_despliegue: pd.DataFrame) -> str:
    
    campania = get_campania(df_datos_campanias = df_datos_campanias)

    df_unicos = get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_campanias = df_datos_campanias)
    fechas_campanias_unicos = df_unicos["fecha_hora_de_embarque"].tolist()
    campanias_unicos = df_unicos["campania"].tolist()
    
    numero_total_de_sondas = get_numero_de_sondas(df_datos_despliegue = df_datos_despliegue)
    
    es_una_campania = True if len(df_unicos) == 1 else False
    p = obtener_palabras_singulares_plurales(es_singular = es_una_campania)
    
    texto = f"Posteriormente, para {p['la_las']} {p['campania_campanias']}, se planeó la logística de {p['la_las']} {p['embarcacion_embarcaciones']} en"
    texto += f" {p['la_las']} {p['cual_cuales']} se transportaron las sondas al lugar del despliegue."
    texto += f" {p['La_Las']} {p['liberacion_liberaciones']} de las {numero_total_de_sondas} sondas se" 
    
    if es_una_campania:
        texto += f" llevó a cabo el {timestamp_a_texto_espanol(fechas_campanias_unicos[0], mes_y_anio = False)}"
    
    else:
        texto += f" {p['dividio_dividieron']} en {len(campanias_unicos)} {p['campania_campanias']};"
    
        for i, (fecha_campania, campania) in enumerate(zip(fechas_campanias_unicos, campanias_unicos)):
            cantidad_de_sondas_por_campania = df_datos_campanias[df_datos_campanias["campania"] == campania].shape[0]
            if i == 0:
                texto += f" {cantidad_de_sondas_por_campania} sondas se liberaron el {timestamp_a_texto_espanol(fecha_campania, mes_y_anio = False)}"
            
            elif i < len(fechas_campanias_unicos) - 1:
                texto += f", {cantidad_de_sondas_por_campania} sondas se liberaron el {timestamp_a_texto_espanol(fecha_campania, mes_y_anio = False)}"       
            
            elif i == len(fechas_campanias_unicos) - 1:
                texto += f" y {cantidad_de_sondas_por_campania} sondas se liberaron el {timestamp_a_texto_espanol(fecha_campania, mes_y_anio = False)}"
            
    texto += f". La ruta de liberación de las sondas en {p['la_las']} {p['campania_campanias']},"
    texto += f" obedeció el trayecto óptimo considerando la distancia desde tierra hasta el lugar de liberación acordado con PEMEX,"
    texto += f" teniendo en cuenta las condiciones atmosféricas y las posiciones en las cuales se hicieron las liberaciones."
    texto += f" El derrotero consideró el sitio donde se dispuso del equipo que se utilizó para la liberación de las sondas y los"
    texto += f" implementos adicionales que se utilizaron para las maniobras costa afuera. Es importante mencionar que el derrotero"
    texto += f" de {p['la_las']} {p['embarcacion_embarcaciones']} pudo estar sujeto a cambios de acuerdo a las condiciones atmosféricas el día del zarpe,"
    texto += f" y a las decisiones que el encargado de la embarcación consideró mejor para salvaguardar la seguridad de toda la"
    texto += f" tripulación. Una vez realizado el plan de crucero de {p['la_las']} {p['campania_campanias']}"
    texto += f", {p['este_estos']} {p['fue_fueron']} {p['enviados_enviaron']} a PEMEX para su autorización, previo a la ejecución de"
    texto += f" {p['la_las']} {p['campania_campanias']}, y de acuerdo con lo acordado en el Contrato No. 658225821"
    
    return texto





