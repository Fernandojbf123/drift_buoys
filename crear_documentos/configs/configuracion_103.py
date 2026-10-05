
#### Configuracion del documento 10.1. ###
### Los parámetros a modificar son la hoja del excel para el mes de vigencia ###
doc_config = {
    "orden_de_servicio": "393",
    "fecha_de_solicitud": "13 de agosto de 2026",

    "ruta_a_carpeta_de_las_figuras": "\\Med_2025-2026\\Reportes_Edit\\Reporte_10.3\\202609\\documento_11",
    "ruta_a_carpeta_de_guardado_del_documento": "\\Med_2025-2026\\Reportes_Edit\\Reporte_10.3\\202609\\documento_11\\documento",
    
    # Necesarios del 10.1 para el 10.3
    "ruta_a_la_carpeta_de_despliegue": "\\Med_2025-2026\\Reportes_Edit\\Reporte_10.1\\202609\\documento_11\\documento",
    "nombre_del_excel_de_porcentajes": "porcentajes_de_las_sondas.xlsx",

    # Excel con las rutas a figuras y descripción de figuras
    "ruta_al_excel_para_crear_documento": "\\Med_2025-2026\\General\\Sondas_DORIS\\2026_info_documentos_103.xlsx",
    "hoja_del_excel_para_crear_documento": "09_1", # "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12" 
    
    # No suelen modificarse
    "nombre_de_salida_del_documento": "ASM-CICESE-Concepto_10.3",
    "ruta_al_excel_de_despliegue_de_sondas": "\\Med_2025-2026\\General\\base_de_datos_planes_de_crucero_y_doris.xlsx",
    "hoja_del_excel_de_despliegue_de_sondas": "despliegue_doris",
    "rutal_al_excel_de_campanias": "\\Med_2025-2026\\General\\base_de_datos_planes_de_crucero_y_doris.xlsx",
    "hoja_del_excel_de_campanias": "campanias",
    "ruta_a_la_plantilla_de_word": "\\Med_2025-2026\\Reportes_Edit\\Plantillas\\Concepto.10.3\\Concepto_10.3_Mediciones_DORIS_plantilla.docx",
    "ruta_a_carpeta_de_plantilla": "\\Med_2025-2026\\Reportes_Edit\\Plantillas\\Concepto.10.3",
    "ruta_a_carpeta_de_planes_de_crucero": "\\Med_2025-2026\\Reportes_Edit\\Planes_de_crucero\\Documentos\\rev",
    "usar_NAS": True, # Indica si se quiere usar la ruta al NAS (True) o las rutas relativas (False). Si se usa el NAS, las rutas relativas se concatenarán a la ruta al NAS. Si no se usa el NAS, se usarán las rutas relativas tal cual están definidas.


}

