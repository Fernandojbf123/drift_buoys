import numpy as np
import pandas as pd
from matplotlib.axes import Axes    
import matplotlib.dates as mdates

def graficar_serie_de_tiempo(axe: Axes, datos: pd.DataFrame, var_name: str, tspan_num: np.ndarray) -> Axes:
    """
    Descripción:
        Grafica una serie de tiempo como puntos individuales en un axis de matplotlib.
        Los datos se muestran como marcadores negros sin líneas conectoras, ideal para
        visualizar observaciones discretas en el tiempo.

    Parámetros:
        axe (matplotlib.axes.Axes): Objeto Axes donde se graficará la serie de tiempo.
        datos (pd.DataFrame): DataFrame que contiene los datos de la serie temporal.
        var_name (str): Nombre de la columna en el DataFrame que contiene los valores a graficar.
        tspan_num (np.ndarray): Array de fechas en formato numérico de matplotlib para el eje X.

    Retorna:
        matplotlib.axes.Axes: El mismo objeto Axes con la serie de tiempo graficada.

    Ejemplo:
        >>> import matplotlib.pyplot as plt
        >>> import matplotlib.dates as mdates
        >>> import pandas as pd
        >>> import numpy as np
        >>> # Crear datos de ejemplo
        >>> fechas = pd.date_range('2025-01-01', periods=100, freq='H')
        >>> datos = pd.DataFrame({
        ...     'Hs': np.random.rand(100) * 2.5,
        ...     'Tp': np.random.rand(100) * 10 + 5
        ... })
        >>> # Convertir fechas a formato numérico matplotlib
        >>> tspan_num = mdates.date2num(fechas)
        >>> # Crear figura y graficar
        >>> fig, ax = plt.subplots()
        >>> ax = graficar_serie_de_tiempo(ax, datos, 'Hs', tspan_num)
        >>> plt.show()

    Notas:
        - La función valida que var_name exista en el DataFrame antes de graficar.
        - Los puntos se grafican con marcador '.' de tamaño 3 en color negro.
        - No se dibujan líneas entre los puntos (linestyle='None').
        - La etiqueta de la serie corresponde al nombre de la variable.

    Raises:
        ValueError: Si la columna var_name no existe en el DataFrame.

    Funciones auxiliares:
        Ninguna

    Categoría:
        Gráficos
    """

    if var_name not in datos.columns:
        raise ValueError(f"La columna '{var_name}' no existe en el DataFrame.")

    varValue = datos[var_name]
    axe.plot(tspan_num, 
                    varValue, 
                    marker='.', 
                    markersize=3,
                    linestyle='None', 
                    color="black", 
                    label=var_name)

    return axe