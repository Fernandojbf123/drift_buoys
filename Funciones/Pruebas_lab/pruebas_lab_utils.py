import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv

################### NO TOCAR #####################
load_dotenv() # Cargar variables de entorno desde el archivo .env
lat = float(os.getenv("lat_coe"))
lon = float(os.getenv("lon_coe"))
coordenadas={
    "lat": lat,
    "lon": lon
}

###############################
def crear_fechas_aleatorias(fecha_inicio: str, fecha_fin: str, periodo: int, variacion: int) -> pd.DatetimeIndex: 
    """" 
    Crea una lista de fechas aleatorias entre fecha_inicio y fecha_fin.
    Las fechas se generan con un periodo fijo y una variacion en segundos.
    Periodo en minutos
    variación en minutos
    """
        
    fechas = []
    current_time = fecha_inicio
    while current_time <= fecha_fin:
        current_time = current_time + pd.Timedelta(minutes=periodo) + pd.Timedelta(minutes=np.random.randint(0, variacion))
        current_time = current_time.replace(second=0)
        fechas.append(current_time)
    return fechas

##############################
def convertir_datetime_a_str(fechas: pd.DatetimeIndex) -> list:
    """
    Convierte un pd.DatetimeIndex a una lista de strings con formato 'YYYY-mm-ddTHH:MM:00.000z'.
    Ejemplo: '2025-12-01T11:39:00.000z'
    """
    return [fecha.strftime('%Y-%m-%dT%H:%M:00.000z') for fecha in fechas]

###############################
def generar_datos(fecha_inicio: pd.Timestamp, 
                  fecha_fin: pd.Timestamp,
                  periodo: int, 
                  variacion: int) -> dict:
   
    output_dic = {
        "fecha": [],
        "latitud": [],
        "logitud": [],
        "speed": [],
        "distance": [],
        "direction": [],
        "direction_gen": [],
        "temp": [],
        "volt": []
    }
    
    fechas = crear_fechas_aleatorias(fecha_inicio, fecha_fin, periodo, variacion)
    fechas_str = convertir_datetime_a_str(fechas)
    
    lat = coordenadas["lat"]
    lon = coordenadas["lon"]
    
    for fecha in fechas_str:
        output_dic["fecha"].append(fecha)
        output_dic["latitud"].append(round(lat+np.random.random()*0.0004,6))
        output_dic["logitud"].append(round(lon+np.random.random()*0.0004,6))
        output_dic["speed"].append(0)
        output_dic["distance"].append(0)
        output_dic["direction"].append(0)
        output_dic["direction_gen"].append("N")
        output_dic["temp"].append(-99)
        output_dic["volt"].append(42+np.random.randint(-2,2))

    return output_dic
