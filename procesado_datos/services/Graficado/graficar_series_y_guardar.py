import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv


from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig
from procesado_datos.services.Graficado.base.Gra_series_de_tiempo_telemetria import Gra_series_de_tiempo_telemetria
from procesado_datos.services.Utils.utilidades import *
################################################################################


def graficar_series_y_guardar(datos: dict, ruta_a_carpeta_de_guardado: str, mostrar_figura:bool=False, config: ProcesadoConfig | None = None) -> None:
    """
    Descripción:
        Función envoltorio que recorre un diccionario de DataFrames (uno por sonda)
        y genera una figura con 10 subplots para cada sonda:
        - 5 series de tiempo (izquierda): Temp, u, v, Rap, Dir
        - 5 histogramas (derecha): uno por cada serie de tiempo

    Parámetros:
        Ninguno (lee desde configuración general)

    Retorna:
        None
        Genera y muestra las figuras para cada sonda en el diccionario.

    Ejemplo:
        graficar_series_y_guardar()

    Funciones auxiliares:
        - cargar_diccionario_pickle
        - Gra_series_de_tiempo_telemetria
    """
    
    seriales_de_sondas = config.seriales_de_sondas  # Obtener los seriales de las sondas desde el diccionario de datos
    
    # Recorrer cada sonda en el diccionario
    for serial in seriales_de_sondas:

        if serial not in datos:
            print(f"Advertencia: Serial {serial} no encontrado en los datos")
            continue

        df = datos[serial]
        # Generar figura para los datos a graficar seleccionados en configuración
        fig, tituloFigura = Gra_series_de_tiempo_telemetria(
            dataFrame=df, 
            NS_sonda=serial, 
            tspan_column='tspan_rounded',
            mostrar_figura=mostrar_figura,
            config=config
        )

        
        # Guardar figura
        nombre_archivo = f"transmision_{serial}"
        guardar_figura(
            figura=fig,
            ruta_a_carpeta=ruta_a_carpeta_de_guardado,
            nombre_archivo=nombre_archivo,
            formato=config.formato_de_figuras,
            resolucion=config.resolucion_de_figuras
        )
