from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *


def ejecucion_de_la_campania_parrafo3(dic_datos_doris: dict) -> str:
    
    df_unicos= get_fecha_y_hora_de_embarque_y_campania_unicos(dic_datos_doris)
    asm = df_unicos["campania"].unique()
    fecha = df_unicos["fecha_hora_de_embarque"].iloc[0]
    fecha_campania = fecha.strftime("%d de %B de %Y") 
    mes_campania = fecha.strftime("%B")
    anio_campania = fecha.strftime("%Y")
    articulo = "la" if len(df_unicos) == 1 else "las"
    palabra_campanias = "campaña" if len(df_unicos) == 1 else "campañas"
    instalaciones = f"{articulo} {palabra_campanias} ({asm.iloc[0]} y {asm.iloc[1]}) es similar en ambos casos"
    
    texto_singular = f"Las actividades asociadas a la ejecución de {articulo} {palabra_campanias} {asm.iloc[0]} realizada el {fecha_campania} de {mes_campania} de {anio_campania} se describe a continuación."
    texto_plural = f"Dado que las actividades asociadas a la ejecución de {instalaciones}, a continuación, se describe la ejecución de la campaña {asm.iloc[0]} realizada el {fecha_campania} de {mes_campania} de {anio_campania}."
    
    texto = texto_singular if len(df_unicos) == 1 else texto_plural
  
    return texto
