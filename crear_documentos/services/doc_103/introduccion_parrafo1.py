from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *

def introduccion_parrafo1(df_datos_campanias: pd.DataFrame, df_datos_despliegue: pd.DataFrame) -> str:

    numero_de_sondas = get_numero_de_sondas(df_datos_despliegue = df_datos_despliegue)
    df_unicos= get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_campanias = df_datos_campanias)
    fechas_campanias_unicos = df_unicos["fecha_hora_de_embarque"].tolist()
    campanias_unicos = df_unicos["campania"].tolist()
    
    texto = f' Como parte del Servicio de Medición y Análisis Metoceánicos del '
    texto+= f'Golfo de México (Contrato No. 658225821), que se lleva a cabo por '
    texto+= f'el consorcio All Solutions de México S. A. de C. V. (en lo sucesivo, ASM) '
    texto+= f'y el Centro de Investigación Científica y Educación Superior de Ensenada '
    texto+= f'(en lo sucesivo, CICESE), ' 
    
    
    lineas_intermedias = ""
    for i, (fecha_campania, campania) in enumerate(zip(fechas_campanias_unicos, campanias_unicos)):
        
        if i == 0:
            lineas_intermedias += f"el día {timestamp_a_texto_espanol(fecha_campania, mes_y_anio = False)} durante la campaña {campania}," 
        
        elif i < len(fechas_campanias_unicos) - 1:
            lineas_intermedias += f"el día {timestamp_a_texto_espanol(fecha_campania, mes_y_anio = False)} durante la campaña {campania} "     
        
        elif i == len(fechas_campanias_unicos) - 1:
            lineas_intermedias += f"y el {timestamp_a_texto_espanol(fecha_campania, mes_y_anio = False)} durante la campaña {campania}," 
            
    final_parrafo = f' se realizaron las liberaciones de {numero_de_sondas} sondas oceanográficas en los puntos específicos '
    final_parrafo+= f'proporcionados por PEMEX en la plataforma continental del Golfo de México '
    
    texto_completo = texto + lineas_intermedias + final_parrafo
    return texto_completo
