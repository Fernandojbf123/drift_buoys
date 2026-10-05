import sys
import logging
import pandas as pd
from configs.manager_doc_config import configuracion_documentos
from services.abrir_plantilla_doris import abrir_plantilla_doris
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *
from services.manager_variables_excel_documento import *
from services.doc_103.constructor_diccionario_datos_documento import *
from services.doc_103.manager_doc103_config import get_ruta_a_carpeta_de_las_figuras
from services.word_template_writer import *
from services.guardar_documento import guardar_documento



def generar_documento_103(doc_config: dict): 

    # Instanciar la clase de las configuraciones del documento
    config = configuracion_documentos(doc_config)

    # Cargar datos de despliegue
    ruta_al_excel_de_campanias = config.get_ruta_al_excel_de_campanias()
    nombre_de_hoja_campanias = config.get_hoja_del_excel_de_campanias()
    df_datos_despliegue = get_datos_de_despliegue(ruta_al_excel_de_campanias, nombre_de_hoja_campanias)
    df_datos_despliegue_filtrado = filtrar_df_datos_despliegue_por_orden_de_servicio(df_datos_despliegue = df_datos_despliegue, orden_de_servicio=config.get_orden_de_servicio(), columna="OS_103")


    seriales_de_sondas = get_seriales_de_sondas(df_datos_despliegue_filtrado)
    
    # Cargar datos de campaña
    df_datos_campanias = get_df_datos_campanias(ruta_al_excel_de_campanias, nombre_de_hoja_campanias)
    df_campanias_filtrado = filtrar_datos_de_campanias(df_datos_campanias=df_datos_campanias, seriales_de_sondas=seriales_de_sondas)
    df_documento = get_df_datos_documento()
    df_porcentajes = get_df_porcentajes()

    # Validar ruta plantilla
    plantilla = get_ruta_a_la_plantilla_de_word()
    if isinstance(plantilla, str) and plantilla.startswith("[CONFIG ERROR]"):
        raise RuntimeError(plantilla)

    doc = abrir_plantilla_doris(plantilla)

    # Usar data filtrada también para figuras para mantener consistencia
    ruta_a_carpeta_de_las_figuras = get_ruta_a_carpeta_de_las_figuras(usar_NAS=True)
    dict_demo = construir_diccionario_agregar_figuras(
        df_datos_documento=df_documento,
        ruta_a_carpeta_de_figuras=ruta_a_carpeta_de_las_figuras,
        df_datos_despliegue=df_datos_despliegue_filtrado,
        df_datos_campanias=df_datos_campanias,
        df_porcentajes=df_porcentajes,
    )

    construir_diccionario_de_portada(df_datos_despliegue=df_datos_despliegue_filtrado,
                                        df_datos_campanias=df_campanias_filtrado,
                                        df_datos_documento=df_documento,
                                        diccionario_de_reemplazos=dict_demo
    )   
    construir_diccionario_de_datos_documento(
        df_datos_despliegue=df_datos_despliegue_filtrado,
        df_datos_campanias=df_campanias_filtrado,
        df_datos_documento=df_documento,
        df_porcentajes=df_porcentajes,
        diccionario_de_reemplazos=dict_demo,
    )

    construir_diccionario_de_reemplazos_para_tablas(
        df_datos_despliegue=df_datos_despliegue_filtrado,
        df_porcentajes=df_porcentajes,
        diccionario_de_reemplazos=dict_demo,
        doc=doc, 
        df_datos_campanias=df_datos_campanias
    )
    
    reemplazar_texto_en_cuadros_de_texto(doc=doc, diccionario_de_reemplazos=dict_demo)
    reemplazar_texto_en_plantilla(doc=doc,diccionario_de_reemplazos=dict_demo)
    insertar_destino_en_marcador(doc=doc,marcador="<<destino_entregable_101>>",bookmark="referencia_entregable_101",numero="1")
    insertar_figuras_en_plantilla(doc=doc, diccionario_de_reemplazos=dict_demo)
    insertar_referencias_cruzadas_en_plantilla(doc=doc, diccionario_de_reemplazos=dict_demo)
    insertar_referencia_en_marcador(doc=doc,marcador="<<ref_entregable_101>>",bookmark="referencia_entregable_101")
    insertar_documento_externo_en_plantilla(doc=doc, diccionario_de_reemplazos=dict_demo)
    rellenar_tablas_en_plantilla(doc=doc,diccionario_de_reemplazos=dict_demo)
    reemplazar_variables_en_tablas(doc=doc, diccionario_de_reemplazos=dict_demo)

    procesar_titulos_y_referencias(doc=doc,diccionario_de_reemplazos=dict_demo)
    activar_actualizacion_de_campos(doc=doc)

    # Calcular fecha para el nombre del documento: primer día del mes siguiente a la vigencia
    fecha_inicio_vigencia = get_fecha_inicio_vigencia(df_datos_despliegue_filtrado)
    if not isinstance(fecha_inicio_vigencia, pd.Timestamp) or pd.isna(fecha_inicio_vigencia):
        raise RuntimeError("Fecha de inicio de vigencia inválida para generar nombre de archivo")
    # primer día del mes siguiente
    fecha_para_nombre = (fecha_inicio_vigencia + pd.DateOffset(months=1)).replace(day=1)
    date_part = fecha_para_nombre.strftime("%Y%m%d")
    nombre_salida = f"ASM-CICESE-Concepto_10.3_{date_part}_00_PRUEBA.docx"
    guardar_documento(doc, nombre_archivo=nombre_salida)