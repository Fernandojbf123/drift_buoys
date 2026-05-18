from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_documento import *

def alcances_parrafo1(dic_datos_doris: dict) -> list[dict[str, str | bool]]:
    
    """ 
    Con base en las especificaciones particulares del Contrato No. 658225821,
    en este documento se reportan las actividades asociadas al concepto “10.1
    Protocolo de liberación de las sondas oceanográficas y transmisión de datos”,
    relacionadas con las sondas oceanográficas liberadas en {mes_y_anio},
    las cuales se ejecutaron para dar cumplimiento a la orden de servicio
    PEMEX-ASM-CICESE-658225821-{orden_de_servicio} e incluyen los siguientes alcances:
    """
    
    orden_de_servicio = get_orden_de_servicio()
    df_documento = get_df_datos_documento()
    anio_de_vigencia = get_variable_documento(df_datos_documento = df_documento, nombre_variable = "anio_de_vigencia")
    mes_de_vigencia = get_variable_documento(df_datos_documento = df_documento, nombre_variable = "mes_de_vigencia")
    mes_y_anio = f"{mes_de_vigencia} de {anio_de_vigencia}"
    
    texto = [
        {"text":"Con base en las especificaciones particulares del Contrato No. 658225821, ", "bold": False},
        {"text":f"en este documento se reportan las actividades asociadas al concepto “10.1 Protocolo de ", "bold": False},
        {"text":f"liberación de las sondas oceanográficas y transmisión de datos”, relacionadas con las sondas oceanográficas ", "bold": False},
        {"text":f"liberadas en {mes_y_anio}, las cuales se ejecutaron para dar cumplimiento a la orden de servicio ", "bold": False},
        {"text":f"PEMEX-ASM-CICESE-658225821-{orden_de_servicio} , ", "bold": True},
        {"text":"e incluyen los siguientes alcances:", "bold": False}
    ]
    
    return texto
