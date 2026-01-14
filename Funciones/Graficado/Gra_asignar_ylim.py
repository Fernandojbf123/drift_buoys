import numpy as np
from matplotlib.ticker import MaxNLocator, MultipleLocator
from matplotlib.ticker import LinearLocator
from matplotlib.ticker import FixedLocator

def Gra_asignar_ylim(var_value, var_name, ax, hist=False, bins=None,fontsize=12):
    
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
    mini = np.nanmin(var_value)
    maxi = np.nanmax(var_value)
    # Calcular el rango y el margen
    range_y = maxi - mini
    padding_factor = range_y * 0.05 # 5% de margen a cada lado
    padding_y = range_y * padding_factor

    # Variables que empiezan en 0
    if var_name.lower() in ["rap_corriente","Hs", "Hm", "Tp"]:
        ylim_min = 0      
        ylim_max = maxi + padding_y

    elif var_name.lower() in ["temperatura_mar","temperatura_aire"]:
        ylim_min = np.floor(mini - padding_y)
        ylim_max = np.ceil(maxi + padding_y)

    else:  # Todas las variables que no sean ["rap_corriente","Hs", "Hm", "Tp"] ni direccion
        ylim_min = mini - padding_y
        ylim_max = maxi + padding_y

    # Variables de direccion
    if var_name in ['dir_corriente']:
        ax.set_ylim([0, 360])
        ax.set_yticks([0, 90, 180, 270, 360])
        # Agregar eje secundario con puntos cardinales
        ax_serie_2 = ax.twinx()
        ax_serie_2.set_ylim([0, 360])
        ax_serie_2.set_yticks([0, 90, 180, 270, 360])
        ax_serie_2.set_yticklabels(['N', 'E', 'S', 'W', 'N'], fontsize=12)
        return ax

    # Asignar los ejes
    ax.set_ylim(ylim_min, ylim_max)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    return ax   