import os
import pandas as pd
import numpy as np

from Funciones.Graficado.base.Gra_corrientes_transmision import Gra_corrientes_transmision
from Funciones.Utils.utilidades import cargar_diccionario_pickle, guardar_figura
from Funciones.Utils.utils_get_config_vars import *

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
        graficar_series_y_histogramas()
    
    Funciones auxiliares:
        - cargar_diccionario_pickle
        - Gra_corrientes_transmision
    """

    carpeta_de_guardado_de_datos_procesados = get_carpeta_guardado_datos_procesados()
    seriales_de_sondas = get_seriales_sondas()
    
    ruta_de_archivo = os.path.join(
        carpeta_de_guardado_de_datos_procesados,
        "datos_procesados_sondas_oceanograficas.pkl"
    )
    datos = cargar_diccionario_pickle(ruta_de_archivo)

    # Recorrer cada sonda en el diccionario
    for serial in seriales_de_sondas:
        
        if serial not in datos:
            print(f"Advertencia: Serial {serial} no encontrado en los datos")
            continue
    
        df = datos[serial]        
        # Generar figura con 5 subplots (5 series)
        fig, tituloFigura = Gra_corrientes_transmision(dataFrame=df, NS_sonda=serial, tspan_column='tspan_rounded')
        
        print(f"Figura generada: {tituloFigura}")
        
        # Guardar figura
        guardar_figura(figura=fig, 
                        ruta_a_carpeta=get_carpeta_guardado_figuras(), 
                        nombre_archivo=tituloFigura, 
                        formato=get_formato_figuras(), 
                        resolucion= get_resolucion_de_figuras())
