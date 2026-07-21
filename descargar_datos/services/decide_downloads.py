import datetime
import os
import pandas as pd

def decide_downloads(serial):
    """
    Decidir si se descargan los datos de un serial en función del historial de descargas.
    Si la diferencia entre la fecha actual y la última descarga es menor o igual a 30 minutos devuelve False (para que no se descargue), 
    si es mayor devuelve True (para que se descargue).
    
    Esta funcion es hermana de la función write_downloads_history; las rutas al archivo deben ser las misma en ambas funciones.
    
    """
    
     # Define the path to the downloads history file
    tmp_folder = "descargar_datos/tmp_files/"
    history_file_path = os.path.join(tmp_folder, "downloads_history.csv")
    
    if not os.path.exists(history_file_path):
        return True
    
    dl_hist = pd.read_csv(history_file_path)
     
    # Buscar el serial descargado en el historial de descargas
    dl_hist["serial"] = dl_hist["serial"].astype(str)  # Asegurarse de que los seriales sean de tipo string 
    dl_cropped = dl_hist[dl_hist["serial"] == serial]
    dl_cropped["timestamp"] = pd.to_datetime(dl_cropped["timestamp"])
    last_download = dl_cropped["timestamp"].max()
    current_time = pd.Timestamp.now().replace(microsecond=0, second=0)  # Remove microseconds and seconds for cleaner output
    diff = current_time - last_download
    
    if diff.total_seconds() <= 1800:  # 1800 seconds = 30 minutes
        return False
    
    return True
    