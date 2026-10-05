import os
import shutil


def copiar_archivos(carpeta_de_origen: str, carpeta_de_destino: str, lista_de_archivos: list):
    
    os.makedirs(carpeta_de_destino, exist_ok=True)
    
    if isinstance(lista_de_archivos, list) is False:
        raise ValueError("lista_de_archivos debe ser una lista")
    if not lista_de_archivos:
        raise ValueError("lista_de_archivos no puede estar vacía")

    for nombre_archivo in lista_de_archivos:
        ruta_origen = os.path.join(carpeta_de_origen, nombre_archivo)
        if os.path.isfile(ruta_origen):
            shutil.copy2(ruta_origen, os.path.join(carpeta_de_destino, nombre_archivo))
            print(f"Archivo copiado: {ruta_origen}")
        else:
            print(f"Archivo no encontrado: {ruta_origen}")

    