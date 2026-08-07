import os
import pandas as pd
from procesado_datos.services.Pruebas_lab.pruebas_lab_utils import generar_datos
from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig


def crear_datos_lab(config: ProcesadoConfig):
    
    seriales = config.seriales_de_sondas
    fecha_ini = config.convertir_a_pd_datetime("fecha_de_inicio_pruebas_lab", formato="%Y-%m-%d %H:%M")
    fecha_fin = config.convertir_a_pd_datetime("fecha_de_fin_pruebas_lab", formato="%Y-%m-%d %H:%M")
    
    datos_creados = {}
    for serial in seriales:
        dic = generar_datos(fecha_inicio=fecha_ini, fecha_fin=fecha_fin, periodo=30, variacion=0)
        df = pd.DataFrame(dic)
        datos_creados[serial] = df
       
    return datos_creados