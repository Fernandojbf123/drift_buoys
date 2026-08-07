import os
import pandas as pd

from procesado_datos.despliegue.services.crear_datos_lab import crear_datos_lab
from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig
from procesado_datos.despliegue.services.guardar_datos_lab_csv import guardar_datos_lab_csv
from procesado_datos.services.Graficado.graficar_mapa_de_despliegue import graficar_mapa_de_despliegue
from procesado_datos.services.Graficado.graficar_series_laboratorio_y_guardar import graficar_series_laboratorio_y_guardar
from procesado_datos.services.Utils.utilidades import guardar_diccionario_como_pickle
from procesado_datos.services.Graficado.graficar_mapa_prueba_lab import graficar_mapa_prueba_lab
from procesado_datos.services.Utils.utilidades import *


def manager_crear_datos_lab(config: ProcesadoConfig):
    
    # Pasos:
    # 1. Crear y guardar (en csv) los datos de las pruebas de laboratorio para cada sonda
    datos = crear_datos_lab(config)
    
    # Crear ruta a la carpeta de guardado de datos de laboratorio
    ruta_a_carpeta = config.carpeta_de_guardado_de_datos_lab 
    fecha_del_estudio = config.convertir_a_pd_datetime("fecha_del_estudio", formato="%Y-%m-%d")
    carpeta_del_estudio = f"{fecha_del_estudio.year:04d}{fecha_del_estudio.month:02d}"
    ruta_a_la_carpeta_de_guardado = os.path.join(ruta_a_carpeta, carpeta_del_estudio, "pruebas_lab")
    
    # 2. Guardar datos datos en csv
    guardar_datos_lab_csv(datos, ruta_a_la_carpeta_de_guardado)
    
    # 3. Guardar los datos procesados    
    guardar_diccionario_como_pickle(
        datos, 
        ruta = ruta_a_la_carpeta_de_guardado, 
        nombre_archivo = config.nombre_del_archivo_de_datos_procesados
    )
    
    
    # # 4. Grafica la serie de tiempo de voltaje de cada sonda durante las pruebas de laboratorio
    graficar_series_laboratorio_y_guardar(
        datos, 
        mostrar_figura = False, 
        ruta_a_la_carpeta_de_guardado = ruta_a_la_carpeta_de_guardado,
        config = config
    )
    
    
    # # 5. Grafica el mapa de ubicación de las sondas durante las pruebas de laboratorio
    graficar_mapa_prueba_lab(
        datos, 
        mostrar_figura=False,
        ruta_a_la_carpeta_de_guardado = ruta_a_la_carpeta_de_guardado,
        config = config
    )
    
    # # 6. Grafica el mapa de despliegue
    graficar_mapa_de_despliegue(
        mostrar_figura = False,
        ruta_a_la_carpeta_de_guardado = ruta_a_la_carpeta_de_guardado,
        config = config
    )