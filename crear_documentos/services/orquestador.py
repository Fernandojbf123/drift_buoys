from crear_documentos.services.abrir_plantilla_doris import abrir_plantilla_doris
from crear_documentos.services.crear_diccionario_del_df_excel_maestro import crear_diccionario_del_df_excel_maestro
from services.leer_excel_maestro import leer_excel_maestro
from utils.utils_get_doc_config import *



def crear_documento_de_despliegue():
        
    # Leer datos del excel maestro
    nombre_de_hoja = get_hoja_del_excel()
    df_excel_maestro = leer_excel_maestro(nombre_de_hoja)
    dic_data = crear_diccionario_del_df_excel_maestro(df_excel_maestro)
    plantilla = abrir_plantilla_doris()
    
    return df_excel_maestro