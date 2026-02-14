import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.axes import Axes
import numpy as np


def graficar_mapa_cartopy(axe:Axes, lon_min: float, lon_max: float, lat_min: float, lat_max: float) -> None:
    """
    Descripción:
        Crea un mapa base geográfico usando Cartopy con proyección PlateCarree.
        Incluye líneas de costa, características geográficas (tierra, océano, fronteras,
        lagos y ríos) y etiquetas formateadas de coordenadas en los ejes.

    Parámetros:
        ax (cartopy.mpl.geoaxes.GeoAxesSubplot): Objeto axis de matplotlib con proyección Cartopy.
        lon_min (float): Longitud mínima del área a mostrar (grados, oeste negativo).
        lon_max (float): Longitud máxima del área a mostrar (grados, oeste negativo).
        lat_min (float): Latitud mínima del área a mostrar (grados).
        lat_max (float): Latitud máxima del área a mostrar (grados).

    Retorna:
        None: Modifica el objeto Axes directamente agregando el mapa base y características.

    Ejemplo:
        >>> import matplotlib.pyplot as plt
        >>> import cartopy.crs as ccrs
        >>> # Crear figura con proyección Cartopy
        >>> fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        >>> # Graficar mapa del Golfo de México
        >>> graficar_mapa_cartopy(ax, lon_min=-98, lon_max=-85, lat_min=18, lat_max=31)
        >>> plt.title("Golfo de México")
        >>> plt.show()

    Notas:
        - La proyección utilizada es PlateCarree (lat/lon rectangulares).
        - Las líneas de costa tienen resolución de 10m para mayor detalle.
        - Los ticks en los ejes X e Y se generan cada 2 grados automáticamente.
        - Las características incluyen:
          * Tierra (gris claro)
          * Océano (azul claro)
          * Fronteras (línea punteada)
          * Lagos (transparencia 50%)
          * Ríos
        - Los ticks se formatean automáticamente con símbolos de grados (°N, °S, °E, °W).

    Funciones auxiliares:
        Ninguna

    Categoría:
        Gráficos
    """
    axe.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    axe.coastlines(resolution='10m')
    axe.add_feature(cfeature.LAND, facecolor='lightgray')
    axe.add_feature(cfeature.OCEAN, facecolor='lightblue')
    axe.add_feature(cfeature.BORDERS, linestyle=':')
    axe.add_feature(cfeature.LAKES, alpha=0.5)
    axe.add_feature(cfeature.RIVERS)

    # Agregar ticks en los ejes X (longitud) e Y (latitud)
    if abs(lon_min) - abs(lon_max) <= 5:
        delta_tick = 0.5
    else:
        delta_tick = 2
        
    xticks = list(np.arange(np.floor(lon_min), np.ceil(lon_max)+1, delta_tick))
    yticks = list(np.arange(np.floor(lat_min), np.ceil(lat_max)+1, delta_tick))
    axe.set_xticks(xticks, crs=ccrs.PlateCarree())
    axe.set_yticks(yticks, crs=ccrs.PlateCarree())

    # Formatear etiquetas de los ticks
    axe.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
    axe.yaxis.set_major_formatter(LATITUDE_FORMATTER)
