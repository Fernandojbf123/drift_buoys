import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

from Funciones.Utils.utils_get_config_vars import *

def graficar_batimetria_en_mapa(ax, datos_de_batimetria) -> None:
    """
    Grafica datos de batimetría en el mapa dado.
    ax: axis de matplotlib donde se graficará la batimetría
    lon, lat: mallas de longitudes y latitudes
    elevation: matriz 2D con datos de elevación (batimetría)
    """
    lon = datos_de_batimetria["lon"]
    lat = datos_de_batimetria["lat"]
    elevation = datos_de_batimetria["elevation"]
    curvas_de_batimetria = datos_de_batimetria["curvas_de_batimetria"]
    
    # Graficar líneas de contorno de batimetría en el mapa
    contornos = ax.contour(lon, lat, elevation, levels=curvas_de_batimetria, colors='gray', linestyles='--', linewidths=0.8)
    # Etiquetar cada curva de nivel con su profundidad: Esto se hizo de forma "automática". Busca el punto más cercano a una posición manual
    # se van definiendo las posiciones donde se pondrán las etiquetas para cada nivel.
    manual_positions = []
    lat = 22
    lon = -100
    for seglist in contornos.allsegs:
        lat -= 0.5
        lon += 0.5
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
    ax.clabel(contornos, fmt='%d', fontsize=get_tamanio_letra()-5, colors='black', manual=manual_positions, inline=True, inline_spacing=5)


    # ax.clabel(contornos, fmt='%d', fontsize=get_tamanio_letra()-1, colors='black', inline=True, inline_spacing=10)
    return None