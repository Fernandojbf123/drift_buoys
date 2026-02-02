general_config = {
    # 1. De la carga
    # cada cuanto tiempo debe medir y enviar información la sonda. Opciones: "1h", "0.5h"
    "delta_tiempo": "0.5h",
    # Ruta al archivo excel con información de las sondas
    "ruta_al_excel_de_despliegue_de_sondas": "Med_2025-2026/General/Sondas_DORIS/2026_01_despliegues_de_DORIS",
    # Formato: 'AAAA-MM-DD HH:MM:SS'
    "fecha_de_inicio_del_analisis": "2026-01-01 00:00:00",
    # Formato: 'AAAA-MM-DD HH:MM:SS'
    "fecha_de_fin_del_analisis": "2026-01-31 23:59:59",
    # Ruta a la carpeta con los datos crudos
    "carpeta_de_datos_crudos": "Med_2025-2026/Reportes_Edit/Reporte_10.3/202601/datos_crudos",
    "cantidad_de_decimales": 4,  # Cantidad de decimales a los que se redondearán los datos
    # Ruta a los datos de batimetría del GOM
    "ruta_a_datos_batimetria": "C:/programacion/codigos_python/bases_de_datos/batimetria_GEBCO_GOM_2023.nc",

    # Lista de seriales de sondas a analizar
    "seriales_de_sondas": ["4876187", "4878196", "4878205", "4878218","4866704","4878221","4878503","4876191","4876190"],
    # "seriales_de_sondas": ["4878503"],

    # 2. Del guardado
    # Ruta a la carpeta para guardar los datos procesados
    "carpeta_de_guardado_de_datos_procesados": "C:/Users/Atmosfera/Desktop/datos_procesados/doris/202601",
    # Nombre del archivo para guardar los datos procesados (formato pickle)
    "nombre_del_archivo_de_datos_procesados": "datos_procesados_sondas_oceanograficas",
    "nombre_del_archivo_de_datos_previos_a_la_fecha_de_estudio": "datos_previos_al_estudio",
    "nombre_del_excel_de_porcentajes": "porcentajes_de_las_sondas",
    # Ruta a la carpeta para guardar las figuras
    "carpeta_de_guardado_de_figuras": "C:/Users/Atmosfera/Desktop/datos_procesados/doris/202601",

    # 3. De las figuras
    # 3.1. Generales
    "formato_de_figuras": "png",  # Opciones: 'png', 'jpg', 'svg', 'pdf'
    "resolucion_de_figuras": 300,  # en dpi
    "origen_de_los_datos": "REALT",  # Opciones: 'REALT', 'MEM'
    "decimales_en_figuras": 2,  # Cantidad de decimales a mostrar en las figuras
    "tipo_de_letra": "Arial",  # Opciones: 'Arial', 'Times New Roman', 'Calibri'
    "tamanio_de_letra": 12,  # Tamaño de letra en las figuras
    "numero_de_bins_histograma": 30,  # Número de bins en los histogramas
    # 3.2. De las series de tiempo
    # Variables a graficar en las series de tiempo y su orden
    "variables_a_graficar": ["temperatura_mar", "u_corriente", "v_corriente", "rap_corriente", "dir_corriente","voltaje"],
    
    # 3.3. Del mapa de trayectorias
    "coordenadas_del_mapa": {"lon_min": -98, 
                             "lon_max": -90, 
                             "lat_min": 18, 
                             "lat_max": 26},
    "escala_de_color_rapidez": {"minimo": 0.0, "maximo": 1.5},  # en m/s
    "graficar_trayectorias_pasadas": True,  # Si se grafican las trayectorias previas a la fecha de estudio
    "curvas_de_batimetria": [-25, -100, -500, -1000, -2000],  # en metros
}
