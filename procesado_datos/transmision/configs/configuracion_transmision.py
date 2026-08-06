config_transmision = {

    # 1. Principales editables por el usuario
    "fecha_del_estudio": "2026-07-01", # Fecha de estudio para el análisis de datos
    "fecha_de_inicio_del_analisis": "2026-07-01 00:00", # Formato: 'AAAA-MM-DD HH:MM'
    "fecha_de_fin_del_analisis": "2026-07-31 23:59", # Formato: 'AAAA-MM-DD HH:MM'
    
    # Para informes 10.3
    "carpeta_de_datos_crudos": "C:\\Users\\Atmosfera\\Desktop\\datos_crudos\\doris\\todos_los_datos",
    "carpeta_de_guardado_de_datos_procesados": "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\doris\\10.3",
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
    # "seriales_de_sondas" : ["4857577", "4909282", "4912199", "4912171", "4907604"], # 27 de junio  2026
    "seriales_de_sondas" : ["4912208","4912223", "9909282", "4912205","4912209"], # 20 de julio 2026
    
    "origen_de_los_datos": "REALT",  # Opciones: 'REALT', 'MEM'
    # 3. Del guardado
    # Ruta a la carpeta para guardar los datos procesados
    # Nombre del archivo para guardar los datos procesados (formato pickle)
    "nombre_del_archivo_de_datos_procesados": "datos_procesados_sondas_oceanograficas",
    "nombre_del_archivo_de_datos_previos_a_la_fecha_de_estudio": "datos_previos_al_estudio",
    "nombre_del_excel_de_porcentajes": "porcentajes_de_las_sondas",

    
    # 4.3. Del mapa de trayectorias
    "coordenadas_del_mapa": {"lon_min": -98,
                             "lon_max": -90,
                             "lat_min": 18,
                             "lat_max": 26},
    "escala_de_color_rapidez": {"minimo": 0.0, "maximo": 1.5},  # en m/s
    
}

