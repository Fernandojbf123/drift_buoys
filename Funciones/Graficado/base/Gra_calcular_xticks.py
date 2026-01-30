import numpy as np
import pandas as pd
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
    
    diferencia = fecha_final.normalize() - fecha_inicial.normalize() + pd.Timedelta(days=1)
    
    if diferencia.days >=6:
        # ticks cada día
        ticks = pd.date_range(
            start=fecha_inicial.normalize(),
            end=fecha_final.normalize(),
            freq='D'
        )
        
        xlim = (fecha_inicial.normalize() - pd.Timedelta(days=1), fecha_final + pd.Timedelta(days=1))
        formato_ticks = "days"
    
    
    elif diferencia.days < 6  and diferencia.days >2:
        # ticks cada día
        ticks = pd.date_range(
            start=fecha_inicial.normalize(),
            end=fecha_final.normalize(),
            freq='D'
        )
        n_ticks = diferencia.days
        
        xlim = (fecha_inicial.normalize() - pd.Timedelta(hours=2), fecha_final + pd.Timedelta(hours=2))
        formato_ticks = "days"
    
    elif diferencia.days <= 2:
        ticks = pd.date_range(
            start=fecha_inicial,
            end=fecha_final,
            freq='h'
        )
        
        xlim = (fecha_inicial - pd.Timedelta(hours=1), fecha_final + pd.Timedelta(hours=1)) 
        formato_ticks = "hours"
    
    # seleccionar n_ticks equiespaciados (Deben ser 5 salvo que sea el caso (entre 3 y 4 días))
    if len(ticks) >= n_ticks:
        # 5 índices equiespaciados, siempre el primero y el último
        indices = np.linspace(0, len(ticks)-1, n_ticks, dtype=int)
        ticks = ticks[indices]
            
    return xlim, ticks, formato_ticks
