import numpy as np
import pandas as pd
from Funciones.Graficado.Gra_calcular_ylim import Gra_calcular_ylim
from matplotlib.lines import Line2D
 
def Gra_serie_de_tiempo(dataFrame, var_name, tspan, ax):
    """
    Descripción:
        Genera una serie de tiempo sobre el eje 'ax' proporcionado
    """

    if var_name not in dataFrame.columns:
        raise ValueError(f"La columna '{var_name}' no existe en el DataFrame.")

    colors = ['k', 'b', 'r', 'm', 'c']

    varValue = dataFrame[var_name]
    ax.plot(tspan, varValue, marker='.', markersize=3,
            linestyle='None', color=colors[0], label=var_name)
    ax.grid()
    
    return ax
