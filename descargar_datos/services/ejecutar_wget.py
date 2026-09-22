import subprocess
import shutil

def ejecutar_wget(url, ruta_de_descarga):
    """
    Ejecuta el comando wget para descargar un archivo desde la URL especificada y guardarlo en la ruta de descarga.
    
    :param url: URL del archivo a descargar.
    :param ruta_de_descarga: Ruta completa donde se guardará el archivo descargado.
    """
    found_error = False
    
    # Buscar si wget y curl están disponibles en el sistema
    wget_path = shutil.which("wget")
    curl_path = shutil.which("curl")
    
    if not wget_path and not curl_path:
        found_error = True
        print("No se pudo ejecutar wget, tampoco curl. Verifica que wget esté instalado y accesible desde la línea de comandos.")
        print("Descarga wget para windows desde https://ftp.gnu.org/gnu/wget/wget-1.21.4.tar.gz")
        print("O también búsca la versión wget-1.21.4.tar.gz en https://ftp.gnu.org/gnu/wget/ ")
        print("Descomprmime, instala y luego agrega el path a wget.exe a tus variables de entorno PATH de Windows")
        print("Después de instalar wget correctamente, reinicia el PC para que los cambios en las variables de entorno surtan efecto.")
        return found_error
        
    # Primero intenta descargar con wget
    if wget_path:
        try: 
            subprocess.run([
                "wget",
                "-O", ruta_de_descarga,
                "-q",  # Modo silencioso
                "--timeout=10",  # Tiempo de espera de 10 segundos
                url
            ], check=True)
        
        except Exception as e:  
            found_error = True
            
    # Si no hay wget disponible, intenta con curl
    else:
        print(f"Error al ejecutar wget, intentando con curl")
        found_error = False
        try: 
            subprocess.run([
                "curl.exe",
                "--max-time", "10",
                "-v",
                "-o", ruta_de_descarga,
                url
            ], check=True)
        
        except Exception as e:
            found_error = True    
            
    return found_error
    
    