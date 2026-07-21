import os
import subprocess
from time import sleep
from services.route_builder import build_download_url
from services.ejecutar_wget import ejecutar_wget
from services.write_downloads_history import write_downloads_history
from services.decide_downloads import decide_downloads

def download_data(carpeta_de_datos_crudos, seriales_de_sondas):
    
          
    print("Seriales de sondas a descargar:", seriales_de_sondas)
    print("Carpeta de datos crudos:", carpeta_de_datos_crudos)
    
    
    for i, serial in enumerate(seriales_de_sondas):
        url = build_download_url(serial)
        
        print(" ")
        print(f" ******* INICIA DESCARGA {serial} || {i+1}/{len(seriales_de_sondas)} ********  ")
        ruta_de_descarga = os.path.join(carpeta_de_datos_crudos, f"datos_Localizacion_{serial}_TOTAL.csv")
        
        if not decide_downloads(serial):
            print(f"Descarga omitida porque fue descargado recientemente")
            continue  # Skip the download if it was done recently
        
        max_retries = 10  # Número máximo de intentos de descarga
        for intento in range(max_retries):
            
            found_error = ejecutar_wget(url, ruta_de_descarga)
            if not found_error:
                print("DESCARGA EXITOSA")
                write_downloads_history(serial)  # Registrar la descarga exitosa
                break  # Salir del bucle si la descarga fue exitosa
            else:
                print(f"ERROR EN LA DESCARGA, REINTENTANDO {intento + 1}/{max_retries}...")
                sleep(2*intento)  # Esperar antes de reintentar
            
            if intento == max_retries - 1:
                print(f"Error crítico: No se pudo descargar el archivo para el serial {serial} después de {max_retries} intentos.")
                raise FileExistsError(f"********* DETIENIENDO EL PROCESO *********")
            
        print("--------------------------------------------------" )
        
