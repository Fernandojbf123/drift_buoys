config_despliegue = {

    # 1. Fechas y seriales
    "fecha_del_estudio": "2026-10-01", # Indica el mes al que corresponde el estudio (i.e: Si el estudio se hizo en Marzo, pero los datos son de Enero; se coloca enero como fecha del estudio)
    "fecha_de_inicio_pruebas_lab": "2026-10-14 15:00", # Formato: 'AAAA-MM-DD HH:MM:SS'
    "fecha_de_fin_pruebas_lab": "2026-10-15 16:00", # Formato: 'AAAA-MM-DD HH:MM:SS'
    
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
    # "seriales_de_sondas" : ["4912208","4912223", "9909282", "4912205","4912209"], # 20 de julio 2026
    # "seriales_de_sondas" : ["B059-4912225","B063-5340036", "B061-5339989", "B062-5340045", "B064-5340026"], # 12 de agosto 2026
    # "seriales_de_sondas" : ["B066-5340046","B060-5339972", "B065-5340042", "B053-4912198", "B048-4869012"], # 13 de agosto 2026
    # "seriales_de_sondas" :["B056-4912208","4866696","B068-5339830","4878214","4878197"],
    "seriales_de_sondas": ["B074-5339828", "B071-5339826", "B070-5339973", "B076-5339968", "B072-5339652"], # 16 de otubre 2026
    # "seriales_de_sondas": ["B073-5339822", "B048-4869012","B079-5339955","B077-5338569","B051-4909282"], # 16 de otubre 2026
    
    
    # 2. Rutas de guardado
    "carpeta_de_guardado_de_datos_lab": "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\doris\\10.1", # Carpeta donde se guardarán los archivos csv de las pruebas de lab
    "nombre_del_archivo_de_datos_procesados": "pruebas_lab_procesado", # Nombre del archivo pkl que contiene los datos procesados de las pruebas de laboratorio 
    # Nota: Dentro de la carpeta de guardado se creará una subcarpeta con el año y mes
    
    # Rango de coordenadas del mapa (para graficar la ubicación de las sondas durante las pruebas de lab)
    "coordenadas_del_mapa_pruebas_lab": {
        "lon_min": -94,
        "lon_max": -90,
        "lat_min": 18,
        "lat_max": 21
    },
    
    "carpeta_de_datos_crudos": "C:\\Users\\Atmosfera\\Desktop\\datos_crudos\\doris\\todos_los_datos",
}