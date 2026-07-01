import os
import pandas as pd
from configs.manager_configuracion import get_carpeta_de_datos_crudos, get_seriales_sondas

def revisar_anomalias():
    """
    Revisa los archivos de datos descargados para detectar anomalías en los últimos 24 horas.
    Crea un archivo CSV de salida con la información de las anomalías detectadas.
    """
    seriales_de_sondas = get_seriales_sondas()
    carpeta_de_datos_crudos = get_carpeta_de_datos_crudos()

    output_dict = {
        "serial": [],
        "fecha_y_hora_de_ultima_medicion_CST": [],
        "tiene_valores_anomalos_en_las_ultimas_24_horas": [],
    }


    for serial in seriales_de_sondas:
        ruta_al_archivo = os.path.join(carpeta_de_datos_crudos, f"datos_Localizacion_{serial}_TOTAL.csv")
        if os.path.exists(ruta_al_archivo):
            
            try:
                df = pd.read_csv(ruta_al_archivo)
                
            except pd.errors.EmptyDataError:
                print(f"El archivo para el serial {serial} está vacío o no tiene datos válidos.")
                raise FileNotFoundError(f"El archivo para el serial {serial} está vacío o no tiene datos válidos.")
            
            df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%dT%H:%M:%S.%fZ", errors='coerce')  # Convertir la columna 'fecha' a datetime
            # Los datos vienen en hora UTC; cambiarlos a CST
            df["fecha"] = df["fecha"]-pd.Timedelta(hours=6)  # Restar 6 horas para convertir de UTC a CST
            
            today = pd.Timestamp.now().strftime("%Y-%m-%d %H:00")
            yesterday = (pd.Timestamp.now() - pd.Timedelta(days=1))
            df_cortado = df[df["fecha"] >= pd.Timestamp(yesterday)]  # Filtrar por fecha
            
        
            if df_cortado.empty:
                print(f"El archivo para el serial {serial} está vacío.")
                max_fecha = df["fecha"].max().strftime("%d/%m/%y %H:%M")
                output_dict["tiene_valores_anomalos_en_las_ultimas_24_horas"].append(f"No. La sonda fue desactivada el {max_fecha}")
            
            else:
                
                velocidad_mayor_a_2 = df_cortado[df_cortado["speed"] > 2]

                if velocidad_mayor_a_2.empty:
                    output_dict["tiene_valores_anomalos_en_las_ultimas_24_horas"].append("No")
                else:
                    print(" ")
                    print(f"Anomalía de velocidad detectada en el serial {serial}: Velocidad mayor a 2 m/s en los últimos 24 horas.")
                    print(velocidad_mayor_a_2)
                    print(" ")
                    output_dict["tiene_valores_anomalos_en_las_ultimas_24_horas"].append(f"Si")
                    
            output_dict["serial"].append(serial)
            output_dict["fecha_y_hora_de_ultima_medicion_CST"].append(df_cortado["fecha"].max().strftime("%d/%m/%y %H:%M"))
                    

    df_salida = pd.DataFrame(output_dict)
    nombre_de_archivo_de_salida = pd.Timestamp.now().strftime("%Y%m%d_%H") + ".csv"
    ruta_de_salida = os.path.join(carpeta_de_datos_crudos, nombre_de_archivo_de_salida)
    df_salida.to_csv(ruta_de_salida, index=False)