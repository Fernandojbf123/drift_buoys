import subprocess

def ejecutar_wget(url, ruta_de_descarga):
    """
    Ejecuta el comando wget para descargar un archivo desde la URL especificada y guardarlo en la ruta de descarga.
    
    :param url: URL del archivo a descargar.
    :param ruta_de_descarga: Ruta completa donde se guardará el archivo descargado.
    """
    found_error = False
    try:
        subprocess.run([
            "wget",
            "-O", ruta_de_descarga,
            "-q",  # Modo silencioso
            "--timeout=10",  # Tiempo de espera de 10 segundos
            url
        ], check=True)
    except:
        found_error = True
    
    return found_error
    
    