
import os
import pandas as pd
from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig


def guardar_datos_lab_csv(data:dict, ruta_carpeta: str):
        
    os.makedirs(ruta_carpeta, exist_ok=True)

    for serial, df in data.items():
        file_path = os.path.join(ruta_carpeta, f"prueba_en_tierra_{serial}_TOTAL.csv")
        df.to_csv(file_path, index=False)
        print(f"Datos de laboratorio de la sonda {serial} guardados en: {file_path}")