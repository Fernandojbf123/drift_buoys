import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max):
    """
    Grafica un mapa base en el eje ax usando Cartopy con proyección PlateCarree.
    Los límites de zoom se definen por lon_min, lon_max, lat_min, lat_max.
    """
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    # Agregar ticks en los ejes X (longitud) e Y (latitud)
    xticks = list(range(int(lon_min), int(lon_max)+1, 2))
    yticks = list(range(int(lat_min), int(lat_max)+1, 2))
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())

    # Formatear etiquetas de los ticks
    ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
    ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
