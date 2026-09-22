import sys
import logging
import pandas as pd
from configs.manager_doc_config import configuracion_documentos
from services.abrir_plantilla_doris import abrir_plantilla_doris
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_datos_campania import *
from services.manager_variables_excel_documento import *
from services.doc_101.constructor_diccionario_datos_documento import *
from services.word_template_writer import *
from services.guardar_documento import guardar_documento



def generar_documento_101(doc_config: dict): 

    # Instanciar la clase de las configuraciones del documento
    config = configuracion_documentos(doc_config)

    # Cargar datos de despliegue
    ruta_al_excel_de_despliegue = config.get_ruta_al_excel_de_despliegue_de_sondas()
    nombre_de_hoja_despliegue = config.get_hoja_del_excel_de_despliegue_de_sondas()
    df_datos_despliegue = get_datos_de_despliegue(ruta_al_excel_de_despliegue, nombre_de_hoja_despliegue)
    df_datos_despliegue_filtrado = filtrar_df_datos_despliegue_por_orden_de_servicio(df_datos_despliegue = df_datos_despliegue, orden_de_servicio=config.get_orden_de_servicio(), columna="OS_101")

    seriales_de_sondas = get_seriales_de_sondas(df_datos_despliegue_filtrado)
    
    # Cargar datos de campaña
    ruta_al_excel_de_campanias = config.get_ruta_al_excel_de_campanias()
    nombre_de_hoja_campanias = config.get_hoja_del_excel_de_campanias()
    df_campanias = get_df_datos_campanias(ruta_al_excel_de_campanias, nombre_de_hoja_campanias)
    df_campanias_filtrado = filtrar_datos_de_campanias(df_datos_campanias=df_campanias, seriales_de_sondas=seriales_de_sondas)
    
    # Cargar datos del excel para el documento
    ruta_al_excel_para_crear_documento = config.get_ruta_al_excel_para_crear_documento()
    hoja_del_excel_para_crear_documento = config.get_hoja_del_excel_para_crear_documento()
    df_documento = get_df_datos_documento(ruta_al_excel_para_crear_documento, hoja_del_excel_para_crear_documento)

    # Plantilla
    plantilla = config.get_ruta_a_la_plantilla_de_word()
    doc = abrir_plantilla_doris(plantilla)

    # Construir diccionarios (usar df filtrado donde corresponde)
    ruta_a_carpeta_de_las_figuras = config.get_ruta_a_carpeta_de_las_figuras()
    dict_demo = construir_diccionario_agregar_figuras(df_datos_documento=df_documento, 
                                                      ruta_a_carpeta_de_figuras=ruta_a_carpeta_de_las_figuras,
                                                      df_datos_despliegue=df_datos_despliegue_filtrado)

    construir_diccionario_de_portada(df_datos_despliegue=df_datos_despliegue_filtrado,
                                    df_datos_campanias=df_campanias_filtrado,
                                    df_datos_documento=df_documento,
                                    diccionario_de_reemplazos=dict_demo,
                                    orden_de_servicio = config.get_orden_de_servicio()
    )   
    
    construir_diccionario_de_datos_documento(
        df_datos_despliegue=df_datos_despliegue_filtrado,
        df_datos_campanias=df_campanias_filtrado,
        config=config,
        diccionario_de_reemplazos=dict_demo,
    )

    construir_diccionario_de_reemplazos_para_plan_de_cruceros(
        df_datos_despliegue=df_datos_despliegue_filtrado,
        df_datos_campanias=df_campanias_filtrado,
        config=config,
        diccionario_de_reemplazos=dict_demo,
    )

    construir_diccionario_de_reemplazos_para_tablas(
        df_datos_despliegue=df_datos_despliegue_filtrado,
        df_datos_campanias=df_campanias_filtrado,
        df_datos_documento=df_documento,
        diccionario_de_reemplazos=dict_demo,
        doc=doc,
    )

    # Insertar y reemplazar contenido
    reemplazar_texto_en_cuadros_de_texto(doc=doc, diccionario_de_reemplazos=dict_demo)
    insertar_figuras_en_plantilla(doc=doc, diccionario_de_reemplazos=dict_demo)
    insertar_referencias_cruzadas_en_plantilla(doc=doc, diccionario_de_reemplazos=dict_demo)
    reemplazar_texto_en_plantilla(doc=doc, diccionario_de_reemplazos=dict_demo)
    reemplazar_variables_en_tablas(doc=doc, diccionario_de_reemplazos=dict_demo)
    insertar_documento_externo_en_plantilla(doc=doc, diccionario_de_reemplazos=dict_demo)
    rellenar_tablas_en_plantilla(doc=doc, diccionario_de_reemplazos=dict_demo)

    # Guardar documento: generar nombre a partir de fecha de vigencia (primer día del mes siguiente)
    fecha_inicio_vigencia = get_fecha_inicio_vigencia(df_datos_despliegue_filtrado)
    if not isinstance(fecha_inicio_vigencia, pd.Timestamp) or pd.isna(fecha_inicio_vigencia):
        raise RuntimeError("Fecha de inicio de vigencia inválida para generar nombre de archivo")
    
    fecha_para_nombre = (fecha_inicio_vigencia + pd.DateOffset(months=1)).replace(day=1)
    date_part = fecha_para_nombre.strftime("%Y%m%d")
    nombre_salida = f"{config.nombre_de_salida_del_documento}_{date_part}_00.docx"
    guardar_documento(doc, ruta_a_la_carpeta_de_guardado=config.get_ruta_a_carpeta_de_guardado_del_documento(), nombre_archivo=nombre_salida)

    