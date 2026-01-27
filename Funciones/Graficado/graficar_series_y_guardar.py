import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv


from Funciones.Graficado.base.Gra_series_de_tiempo_telemetria import Gra_series_de_tiempo_telemetria
from Funciones.Utils.utils_get_config_vars import *
from Funciones.Utils.utilidades import *
################################################################################


def graficar_series_y_guardar() -> None:
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
    # Cargar datos procesados
    ruta_a_la_carpeta_de_datos_procesados = crear_ruta_a_carpeta(get_carpeta_guardado_datos_procesados())
    nombre_del_archivo_de_datos_procesados = get_nombre_archivo_datos_procesados()
    ruta_de_archivo = os.path.join(ruta_a_la_carpeta_de_datos_procesados, nombre_del_archivo_de_datos_procesados)

    datos = cargar_diccionario_pickle(ruta_de_archivo)

    seriales_de_sondas = get_seriales_sondas()
    # Recorrer cada sonda en el diccionario
    for serial in seriales_de_sondas:

        if serial not in datos:
            print(f"Advertencia: Serial {serial} no encontrado en los datos")
            continue

        df = datos[serial]
        # Generar figura para los datos a graficar seleccionados en configuración
        fig, tituloFigura = Gra_series_de_tiempo_telemetria(
            dataFrame=df, NS_sonda=serial, tspan_column='tspan_rounded')

        # Guardar figura
        guardar_figura(figura=fig,
                       ruta_a_carpeta=crear_ruta_a_carpeta(
                           get_carpeta_guardado_figuras()),
                       nombre_archivo=tituloFigura,
                       formato=get_formato_figuras(),
                       resolucion=get_resolucion_de_figuras())
