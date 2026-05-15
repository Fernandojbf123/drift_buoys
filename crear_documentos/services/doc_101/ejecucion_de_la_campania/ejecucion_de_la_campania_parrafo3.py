from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *


def ejecucion_de_la_campania_parrafo3(dic_datos_doris: dict) -> str:
    
    df_unicos= get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_de_campanias)
    
    numero_de_sondas = get_numero_de_sondas(df_datos_doris)
    
    texto = "Dado que las actividades asociadas a la ejecución de "
#parrafo original : En cada campaña, el líder del equipo de instalación le informó al personal las actividades que se realizarían durante
# el despliegue de las sondas con el fin de que cada miembro del equipo conociera los detalles de la operación, propiciando la integridad del personal
# y de los equipos de dichas sondas; asimismo se siguieron los procedimientos de seguridad durante todas las campañas de despliegue de las sondas oceanográficas.
# Dado que las actividades asociadas a la ejecución de las campañas (ASM-193 y ASM-196) es similar en ambos casos, a continuación, se describe la ejecución 
# de la campaña ASM-193 realizada el 18 de abril de 2026


    if len(df_unicos) == 1:
        asm = df_unicos["campania"].iloc[0]
        fecha = df_unicos["fecha_hora_de_embarque"].iloc[0]
        fecha_campania = fecha.strftime("%d de %B de %Y") 
        
        
        texto = "La ejecución de la campaña de instalación de las sondas, se efectuó de acuerdo con la planeación de la logística y derrotero de la embarcación "
        
        texto += "la campaña " + asm + " realizada el " + fecha_campania,  
        return convertir_texto(texto, numero_de_sondas, numero_de_campanias)
    
    
    else:
        pass
        
    
    texto = conectores_masculinos_o_femeninos(texto) 
    
    texto = f" las campañas ({asm1} y {asm2}) es similar en ambos casos, a continuación, se describe la ejecución de la campaña {asm1} realizada el {fecha_campania1}."
    
    return texto


