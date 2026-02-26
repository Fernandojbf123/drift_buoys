from crear_documentos.services.guardar_documento import guardar_documento
from crear_documentos.services.abrir_plantilla_doris import abrir_plantilla_doris
from crear_documentos.services.crear_diccionario_del_df_excel_maestro import crear_diccionario_del_df_excel_maestro
from crear_documentos.services.reemplazar_en_parrafo import reemplazar_en_word
from services.leer_excel_maestro import leer_excel_maestro
from crear_documentos.configs.manager_doc_config import *



def crear_documento_de_despliegue():
        
    # Leer datos del excel maestro
    nombre_de_hoja = get_hoja_del_excel()
    df_excel_maestro = leer_excel_maestro(nombre_de_hoja)
    diccionario_de_reemplazos = crear_diccionario_del_df_excel_maestro(df_excel_maestro)
    plantilla = abrir_plantilla_doris()
    doc_modificado = reemplazar_en_word(plantilla, diccionario_de_reemplazos)
    guardar_documento(doc_modificado)
    
    return df_excel_maestro