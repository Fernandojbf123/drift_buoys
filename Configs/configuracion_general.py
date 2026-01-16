general_config = {
    # 1. De la carga
    "delta_tiempo": "0.5h", # cada cuanto tiempo debe medir y enviar información la sonda. Opciones: "1h", "0.5h"
    "ruta_al_excel_de_despliegue_de_sondas": "Med_2025-2026/General/Sondas_DORIS/2026_01_despliegues_de_DORIS", # Ruta al archivo CSV con información de las sondas
    "fecha_de_inicio_del_analisis": "2025-12-01 00:00:00", # Formato: 'AAAA-MM-DD HH:MM:SS'
    "fecha_de_fin_del_analisis": "2025-12-31 23:59:59", # Formato: 'AAAA-MM-DD HH:MM:SS'
    "carpeta_de_datos_crudos": "/Med_2025-2026/Reportes_Edit/Reporte_10.3/diciembre/datos_crudos", # Ruta a la carpeta con los datos crudos
    "cantidad_de_decimales": 4, # Cantidad de decimales a los que se redondearán los datos

    "seriales_de_sondas": ["4876187","4878196","4878205","4878218"], # Lista de seriales de sondas a analizar

    # 2. Del guardado
    "carpeta_de_guardado_de_datos_procesados": "Med_2025-2026/Reportes_Edit/Reporte_10.3/diciembre/datos_procesados", # Ruta a la carpeta para guardar los datos procesados
    "nombre_del_archivo_de_datos_procesados": "datos_procesados_sondas_oceanograficas", # Nombre del archivo para guardar los datos procesados (formato pickle)
    "nombre_del_excel_de_porcentajes": "porcentajes_de_las_sondas",
    "carpeta_de_guardado_de_figuras": "Med_2025-2026/Reportes_Edit/Reporte_10.3/diciembre/figuras", # Ruta a la carpeta para guardar las figuras

    # 3. De las figuras
    "formato_de_figuras": "png",  # Opciones: 'png', 'jpg', 'svg', 'pdf'
    "resolucion_de_figuras": 300,  # en dpi
    "origen_de_los_datos": "REALT", # Opciones: 'REALT', 'MEM' 
    "decimales_en_figuras": 2, # Cantidad de decimales a mostrar en las figuras
    "tipo_de_letra": "Arial", # Opciones: 'Arial', 'Times New Roman', 'Calibri'
    "tamanio_de_letra": 12, # Tamaño de letra en las figuras
    "numero_de_bins_histograma": 30, # Número de bins en los histogramas
    "variables_a_graficar": ["temperatura_mar","u_corriente", "v_corriente", "rap_corriente", "dir_corriente"], # Se graficaran series de tiempo e histogramas para estas variables, en ese mismo orden.
}