
import numpy as np
from matplotlib.ticker import MaxNLocator, MultipleLocator
from matplotlib.ticker import LinearLocator
from matplotlib.ticker import FixedLocator

def Gra_calcular_ylim(varValue, varName, ax, hist=False, bins=None, padding_factor=0.08):
    
    """
    Descripción: 
        Ajusta automáticamente los límites del eje Y y las etiquetas de ticks 
        en un gráfico según el rango de valores de la variable.

        Este ajuste se realiza para variables cuyo mínimo esperado es 0, generando etiquetas de eje
        más limpias y legibles.

    Parámetros:
        varValue (array): Serie de datos (puede contener NaNs) correspondiente a la variable a graficar.
        varName (str): Nombre de la variable, usado para determinar si se debe forzar un mínimo en 0.
                       Variables compatibles: "Hs", "Hm", "Tp", "Rap", "Rap1"
        ax (matplotlib.axes): Objeto de eje ('ax') donde se ajustarán los límites y ticks.

    Retorna: El objeto de eje con los límites y ticks de Y ajustados.

        Notas:
            - Si 'varName' pertenece a un conjunto de variables predefinidas, se ajusta el eje Y
              para que inicie en 0 y tenga espaciado uniforme.
            - Se usa 'np.nanmin' y 'np.nanmax' para ignorar valores NaN en los cálculos.
            - La lógica para el espaciado de ticks busca crear divisiones equidistantes y redondeadas.

    Ejemplo:
        ax = Gra_calcular_ylim(df['Hs'], 'Hs', ax)

    Funciones auxiliares: 
        Ninguna
    
    Categoría: 
        Gráficos
    """

    # Define un factor de padding (margen) para series de tiempo
    padding_factor = 0.14  # 5% de margen a cada lado (ajusta si es necesario)
    
    if hist:
    # Lógica para Histogramas: Margen superior fijo (1.5)
        counts, _ = np.histogram(varValue.dropna(), bins=bins)
        maxi = np.max(counts)
        ax.set_ylim(0, maxi * 1.2)  # margen
        ax.yaxis.set_major_locator(MaxNLocator(nbins=5, integer=True))
        
    else:
    # Lógica para Series de Tiempo: Añadir Padding
        mini = np.nanmin(varValue)
        maxi = np.nanmax(varValue)
        
        # Calcular el rango y el margen
        range_y = maxi - mini
        padding_y = range_y * padding_factor

        
        # 🔹 Variables que deben iniciar en 0
        if varName in {"Hs", "Hm", "Tp", "Rap", "Rap1", "Rap2"}:
            ylim_min = 0
            ylim_max = maxi + padding_y
            ax.set_ylim(ylim_min, ylim_max)
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
        
        # 🔹 Variables positivas y negativas (Temp, u, v, etc.)
        else:
            ylim_min = mini - padding_y
            ylim_max = maxi + padding_y
            ax.set_ylim(ylim_min, ylim_max)
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))

    return ax


    
    



    

