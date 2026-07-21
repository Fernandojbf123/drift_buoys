
from services.download_data import download_data

if __name__ == "__main__":
    # Si se ejecuta directamente este script, se obtienen los valores de configuración y se llama a la función download_data
    print("Cargando configuraciones desde el módulo descargar_datos")
    from configs.manager_configuracion import get_seriales_sondas, get_carpeta_de_datos_crudos
    carpeta_de_datos_crudos = get_carpeta_de_datos_crudos() # carpeta donde se guardan los datos crudos 
    seriales_de_sondas = get_seriales_sondas() # Seriales de sondas a descargar
    download_data(carpeta_de_datos_crudos, seriales_de_sondas)
else:
    # Configuraciones heredadas del módulo Procesar_datos
    print("Cargando configuraciones desde el módulo Procesar_datos")
    
    