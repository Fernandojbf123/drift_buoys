from crear_documentos.services.guardar_documento import guardar_documento
from crear_documentos.services.abrir_plantilla_doris import abrir_plantilla_doris
from crear_documentos.services.crear_diccionario_del_df_excel_maestro import crear_diccionario_del_df_excel_maestro
from crear_documentos.services.word_template_writer import (
    insertar_figuras_en_plantilla,
    insertar_referencias_cruzadas_en_plantilla,
    reemplazar_texto_en_plantilla,
    insertar_documento_externo_en_plantilla,
)
from crear_documentos.services.leer_excel import leer_excel
from crear_documentos.configs.manager_doc_config import *



def crear_documento_de_despliegue():
        
    # Leer datos del excel maestro
    nombre_de_hoja = get_hoja_del_excel()
    ruta_al_archivo = get_ruta_al_excel_maestro() + ".xlsx"
    df_excel_maestro = leer_excel(ruta_al_archivo, nombre_de_hoja)
    diccionario_de_reemplazos = crear_diccionario_del_df_excel_maestro(df_excel_maestro)
    plantilla = abrir_plantilla_doris()
    
    # Aplicar todas las transformaciones a la plantilla
    reemplazar_texto_en_plantilla(plantilla, diccionario_de_reemplazos)
    insertar_figuras_en_plantilla(plantilla, diccionario_de_reemplazos)
    insertar_referencias_cruzadas_en_plantilla(plantilla, diccionario_de_reemplazos)
    
    # Insertar documento externo si existe la key en el diccionario
    if "<<ruta_plan_de_crucero>>" in diccionario_de_reemplazos:
        insertar_documento_externo_en_plantilla(plantilla, diccionario_de_reemplazos)
    
    guardar_documento(plantilla)
    
    return df_excel_maestro