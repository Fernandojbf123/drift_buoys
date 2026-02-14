from matplotlib.axes import Axes
import numpy as np
from Funciones.Utils.utils_get_config_vars import *

def graficar_batimetria_en_mapa(axe: Axes, datos_de_batimetria: dict) -> None:
    """
    Descripción:
        Grafica líneas de contorno de batimetría (curvas de nivel de profundidad)
        sobre un mapa de matplotlib/cartopy. Las curvas se dibujan con líneas
        discontinuas grises y se etiquetan automáticamente con valores de profundidad.

    Parámetros:
        axe (matplotlib.axes.Axes): Objeto axis de matplotlib donde se graficará la batimetría.
        datos_de_batimetria (dict): Diccionario con los datos batimétricos que debe contener:
            - "lon" (array 2D): Malla de longitudes (grados).
            - "lat" (array 2D): Malla de latitudes (grados).
            - "elevation" (array 2D): Matriz con datos de elevación/profundidad (metros).
            - "curvas_de_batimetria" (list): Lista de niveles de profundidad a graficar (ej: [-100, -200, -500]).

    Retorna:
        None: Modifica el objeto Axes directamente agregando las curvas de nivel.

    Ejemplo:
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fig, axe = plt.subplots()
        >>> # Crear datos de batimetría de ejemplo
        >>> lon_grid = np.linspace(-100, -95, 50)
        >>> lat_grid = np.linspace(20, 25, 50)
        >>> lon, lat = np.meshgrid(lon_grid, lat_grid)
        >>> elevation = -np.sqrt((lon + 97.5)**2 + (lat - 22.5)**2) * 100  # Profundidad simulada
        >>> datos_batimetria = {
        ...     "lon": lon,
        ...     "lat": lat,
        ...     "elevation": elevation,
        ...     "curvas_de_batimetria": [-100, -200, -500, -1000]
        ... }
        >>> graficar_batimetria_en_mapa(ax, datos_batimetria)
        >>> plt.show()

    Notas:
        - Las etiquetas de profundidad se colocan automáticamente en posiciones
          calculadas para evitar superposiciones.
        - El algoritmo busca el punto más cercano a una posición de referencia
          para cada curva de nivel.
        - Las líneas se dibujan en gris discontinuo con grosor de 0.8.

    Funciones auxiliares:
        - get_tamanio_de_letra(): Obtiene el tamaño de fuente configurado para las etiquetas.

    Categoría:
        Gráficos
    """
    lon = datos_de_batimetria["lon"]
    lat = datos_de_batimetria["lat"]
    elevation = datos_de_batimetria["elevation"]
    curvas_de_batimetria = datos_de_batimetria["curvas_de_batimetria"]
    
    # Graficar líneas de contorno de batimetría en el mapa
    contornos = axe.contour(lon, lat, elevation, levels=curvas_de_batimetria, colors='gray', linestyles='--', linewidths=0.8)
    # Etiquetar cada curva de nivel con su profundidad: Esto se hizo de forma "automática". Busca el punto más cercano a una posición manual
    # se van definiendo las posiciones donde se pondrán las etiquetas para cada nivel.
    manual_positions = []
    lat = 19 #22
    lon = -92.5 #-100
    for seglist in contornos.allsegs:
        lat -= 0.1
        lon += 0.05
        dif = 1000  # valor grande inicial
        if seglist:  # Si hay segmentos para este nivel
            for a , _ in enumerate(seglist):
                for b , _ in enumerate(seglist[a]):
                    x, y = seglist[a][b]  # Primer punto del primer segmento
                    new_dif = np.sqrt((x - lon)**2 + (y - lat)**2)
                    if new_dif < dif:
                        dif = new_dif
                        x_closest, y_closest = x, y
            manual_positions.append((x_closest, y_closest))

    # Ahora coloca una etiqueta en cada posición
    axe.clabel(contornos, fmt='%d', fontsize=get_tamanio_de_letra()-5, colors='black', manual=manual_positions, inline=True, inline_spacing=5)


    # ax.clabel(contornos, fmt='%d', fontsize=get_tamanio_de_letra()-1, colors='black', inline=True, inline_spacing=10)
    return None