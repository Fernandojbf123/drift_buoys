# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 14:23:30 2025

@author: Atmosfera
"""

import pandas as pd
import matplotlib.dates as mdates
import locale


# Meses en español
try:
    locale.setlocale(locale.LC_TIME, "es_ES.utf8")
except:
    locale.setlocale(locale.LC_TIME, "Spanish_Spain")

# def GraTicks_corregido(fecha_inicial, fecha_final, n_ticks=5, margen_derecho=0.01):
#     """
#     Genera n_ticks fechas equiespaciadas y ajusta el límite derecho
#     para que el último tick no quede pegado al borde.
#     """
    
#     fecha_inicial = pd.to_datetime(fecha_inicial)
#     fecha_final = pd.to_datetime(fecha_final)

#     # ticks equiespaciados
#     ticks = pd.date_range(start=fecha_inicial, end=fecha_final, periods=n_ticks)

#     # ampliar el límite derecho (5% del rango por defecto)
#     delta = fecha_final - fecha_inicial
#     fecha_final_expandida = fecha_final + pd.Timedelta(seconds=delta.total_seconds() * margen_derecho)
#     # extender límite derecho para cubrir todo el último día
#     fecha_final_expandida = fecha_final + pd.Timedelta(days=1)

#     return fecha_inicial, fecha_final_expandida, ticks

def Gra_calcular_xticks(tspan: pd.DatetimeIndex, n_ticks:int =5)-> tuple:
    fecha_inicial = tspan.min()
    fecha_final = tspan.max()

    # ticks diarios (solo fechas)
    ticks = pd.date_range(
        start=fecha_inicial.normalize(),
        end=fecha_final.normalize(),
        periods=n_ticks
    )

    # límite derecho: fin completo del último día
    fecha_final_expandida = fecha_final.normalize() + pd.Timedelta(days=1.2)

    return fecha_inicial, fecha_final_expandida, ticks
