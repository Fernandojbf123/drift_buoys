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
        "rapidez_dentro_del_rango": [],
        "voltaje_dentro_del_rango": []
    }


    for serial in seriales_de_sondas:
        ruta_al_archivo = os.path.join(carpeta_de_datos_crudos, f"datos_Localizacion_{serial}_TOTAL.csv")
        if os.path.exists(ruta_al_archivo):
            
            try:
                df = pd.read_csv(ruta_al_archivo)
                
            except pd.errors.EmptyDataError:
                print(f"El archivo para el serial {serial} está vacío o no tiene datos válidos.")
                raise FileNotFoundError(f"El archivo para el serial {serial} está vacío o no tiene datos válidos.")
            
            if df.empty:    
                return f"El archivo para el serial {serial} está vacío o no tiene datos válidos."
            
            print(ruta_al_archivo)
            df.rename(columns={"fecha": "fecha_utc"}, inplace=True)
            df["fecha_utc"] = pd.to_datetime(df["fecha_utc"], format="%Y-%m-%dT%H:%M:%S.%fZ", errors='coerce')  # Convertir la columna 'fecha' a datetime
            # Los datos vienen en hora UTC; cambiarlos a CST
            df["fecha_cst"] = df["fecha_utc"]-pd.Timedelta(hours=6)  # Restar 6 horas para convertir de UTC a CST
            fecha_de_ultima_medicion = df["fecha_cst"].max() # CST
            fecha_de_ultima_medicion_str = df["fecha_cst"].max().strftime("%d/%m/%y %H:%M") # CST

            # Crear un DF filtrado para los últimos 24 horas
            yesterday_tspan = (pd.Timestamp.now() - pd.Timedelta(days=1))
            df_cortado = df[df["fecha_cst"] >= pd.Timestamp(yesterday_tspan)]  # Filtrar por fecha

            # Si el df_cortado está vacío (No hay datos en las últimas 24 horas)
            if df_cortado.empty:
                print(f"El archivo para el serial {serial} no tiene datos en las últimas 24 horas.")
                output_dict["rapidez_dentro_del_rango"].append(f"Sonda desactivada el {fecha_de_ultima_medicion_str}")
                output_dict["voltaje_dentro_del_rango"].append(f"Sonda fue desactivada el {fecha_de_ultima_medicion_str}")
                
            # Si el df_cortado tiene datos (hay datos en las últimas 24 horas)
            else: 
                # Busco si tiene valores anómalos de velocidad
                velocidad_mayor_a_2 = df_cortado[df_cortado["speed"] > 2]
                if velocidad_mayor_a_2.empty:
                    output_dict["rapidez_dentro_del_rango"].append("Si")
                else:
                    print(" ")
                    print(f"Anomalía de rapidez detectada en el serial {serial}: Velocidad mayor a 2 m/s en los últimos 24 horas.")
                    print(velocidad_mayor_a_2)
                    print(" ")
                    output_dict["rapidez_dentro_del_rango"].append(f"No; se detectaron valores anómalos")
                
                # Buscar si existen valores anómalos en el voltaje
                voltaje_menor_a_39 = df_cortado[df_cortado["volt"] <= 39]
                if voltaje_menor_a_39.empty:
                    output_dict["voltaje_dentro_del_rango"].append("Si; entre 40 y 43 V")
                else:
                    print(" ")
                    print(f"Anomalía de voltaje detectada en el serial {serial}: Voltaje menor a 40 V en los últimos 24 horas.")
                    print(voltaje_menor_a_39)
                    print(" ")
                    output_dict["voltaje_dentro_del_rango"].append("No; menor a 40 V")
                    
                # Avisar si dejó de transmitir
                diferencia = (pd.Timestamp.now().normalize() - fecha_de_ultima_medicion).total_seconds()/3600
                if diferencia > 5:
                    print(f"El serial {serial} dejó de transmitir hace más de 5 horas.")
                    
            output_dict["serial"].append(serial)
            output_dict["fecha_y_hora_de_ultima_medicion_CST"].append(fecha_de_ultima_medicion_str)
                    
    df_salida = pd.DataFrame(output_dict)
    nombre_de_archivo_de_salida = pd.Timestamp.now().strftime("%Y%m%d_%H") + ".csv"
    ruta_de_salida = os.path.join(carpeta_de_datos_crudos, nombre_de_archivo_de_salida)
    df_salida.to_csv(ruta_de_salida, index=False)