from configs.manager_doc_config import *
from services.manager_variables_excel_datos_doris import *
from services.manager_variables_excel_datos_campania import *


def ejecucion_de_la_campania_parrafo2(dic_datos_doris: dict) -> str:
    
    df_unicos= get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_de_campanias)
    
    
    
    texto = "Dado que las actividades asociadas a la ejecución de "
    
    
    if len(df_unicos) == 1:
        return "No se encontraron datos de campañas en el archivo Excel."
    
    
    else:
        for index, row in df_unicos.iterrows():
            campania = row["campania"]
            fecha_y_hora_de_campania = row["fecha_hora_de_embarque"]
    
        
    
    texto = conectores_masculinos_o_femeninos(texto) 
    
    texto = f" las campañas ({asm1} y {asm2}) es similar en ambos casos, a continuación, se describe la ejecución de la campaña {asm1} realizada el {fecha_campania1}."
    
    return texto


