general_config = {

    # 1. Principales editables por el usuario
    # Formato: 'AAAA-MM-DD HH:MM:SS'
    "fecha_de_inicio_del_analisis": "2026-06-01 00:00:00", #
    "fecha_de_fin_del_analisis": "2026-06-30 23:59:59",

    # # Para 10.1
    # "carpeta_de_datos_crudos": "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\doris\\10.1\\202605\\pruebas_lab", # Para pruebas de lab
    # "carpeta_de_guardado_de_datos_procesados": "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\doris\\10.1\\202605\\pruebas_lab", # Para pruebas de lab
    # "carpeta_de_guardado_de_figuras": "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\doris\\10.1\\202605\\pruebas_lab", # Para pruebas de lab
    # "variables_a_graficar": ["voltaje"],
    
    # Para informes 10.3
    "carpeta_de_datos_crudos": "C:\\Users\\Atmosfera\\Desktop\\datos_crudos\\doris\\todos_los_datos",
    "carpeta_de_guardado_de_datos_procesados": "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\doris\\10.3\\202606\\",
    "carpeta_de_guardado_de_figuras": "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\doris\\10.3\\202606\\", # Para datos procesados
    "variables_a_graficar": ["temperatura_mar", "u_corriente", "v_corriente", "rap_corriente", "dir_corriente","voltaje"],


     # Lista de seriales de sondas a analizar
    # "seriales_de_sondas": ["4876187", "4878196", "4878205", "4878218","4866704","4878221","4878503","4876191","4876190"], # Todas
    # "seriales_de_sondas": ["4878221", "4878218", "4876187", "4878205", "4878196"], # diciembre 2025
    # "seriales_de_sondas": ["4866704"], # 26 de diciembre 2025
    # "seriales_de_sondas": ["4878221","4878503","4876191","4876190"], # Enero 2026
    # "seriales_de_sondas": ["4878219","4878190","4878213","4878203","4876177"], # 19 febrero 2026
    # "seriales_de_sondas": ["4878219"], # 19 febrero 2026
    # "seriales_de_sondas": ["4878319","4878152","4876178","4878225","4878504"], # 20 febrero 2026
    # "seriales_de_sondas": ["4876179", "4912197", "4887980", "4866660"], # 26 de marzo
    # "seriales_de_sondas": ["4878319"], # 01 Marzo 2026
    # "seriales_de_sondas": ["4878319", "4876179", "4912197", "4887980", "4866660"], # Todos los despliegues de marzo
    # "seriales_de_sondas": ["9878221","9878504", "9878225", "9876178","9878203"], # 18 de abril 2026
    # "seriales_de_sondas": ["4878505","9878218"], # 26 de abril 2026
    #"seriales_de_sondas": ["9878221", "9878504", "9878225", "9876178", "9878203", "4878505", "9878218"], # Todos de abril 2026
    # "seriales_de_sondas": ["4910070","4912213", "4904116", "4901427","4912212"], # 26 de mayo  2026
    "seriales_de_sondas" : ["4857577", "4909282", "4912199", "4912171", "4907604"], # 27 de junio  2026
    
    # 2. De la carga
    # cada cuanto tiempo debe medir y enviar información la sonda. Opciones: "1h", "0.5h"
    "delta_tiempo": "0.5h",
    # Ruta al archivo excel con información de las sondas
    "ruta_al_excel_de_despliegue_de_sondas": "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\base_de_datos_planes_de_crucero_y_doris.xlsx",
    "nombre_de_la_hoja_con_informacion_de_sondas": "despliegue_doris",
    "cantidad_de_decimales": 4,  # Cantidad de decimales a los que se redondearán los datos
    # Ruta a los datos de batimetría del GOM
    "ruta_a_datos_batimetria": "C:\\programacion\\codigos_python\\bases_de_datos\\batimetria_GEBCO_GOM_2023.nc",
     # Ruta a los datos de topografía ETOPO1_Ice_g_gmt4 (se usan para dar los colores de tierra)
    "ruta_a_datos_topografia": "C:\\programacion\\codigos_python\\bases_de_datos\\topografia_ETOPO1_Ice_g_gmt4.nc",

    # 3. Del guardado
    # Ruta a la carpeta para guardar los datos procesados
    # Nombre del archivo para guardar los datos procesados (formato pickle)
    "nombre_del_archivo_de_datos_procesados": "datos_procesados_sondas_oceanograficas",
    "nombre_del_archivo_de_datos_previos_a_la_fecha_de_estudio": "datos_previos_al_estudio",
    "nombre_del_excel_de_porcentajes": "porcentajes_de_las_sondas",

    # 4. De las figuras
    # 4.1. Generales
    "formato_de_figuras": "png",  # Opciones: 'png', 'jpg', 'svg', 'pdf'
    "resolucion_de_figuras": 300,  # en dpi
    "origen_de_los_datos": "REALT",  # Opciones: 'REALT', 'MEM'
    "decimales_en_figuras": 2,  # Cantidad de decimales a mostrar en las figuras
    "tipo_de_letra": "Arial",  # Opciones: 'Arial', 'Times New Roman', 'Calibri'
    "tamanio_de_letra": 12,  # Tamaño de letra en las figuras
    "numero_de_bins_histograma": 30,  # Número de bins en los histogramas
    # 4.2. De las series de tiempo
    # Variables a graficar en las series de tiempo y su orden

    # 4.3. Del mapa de trayectorias
    "coordenadas_del_mapa": {"lon_min": -98,
                             "lon_max": -90,
                             "lat_min": 18,
                             "lat_max": 26},
    "escala_de_color_rapidez": {"minimo": 0.0, "maximo": 1.5},  # en m/s
    "graficar_trayectorias_pasadas": False,  # Si se grafican las trayectorias previas a la fecha de estudio
    "curvas_de_batimetria": [-25, -100, -500, -1000, -2000],  # en metros
}