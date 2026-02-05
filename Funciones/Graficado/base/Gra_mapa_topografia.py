import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap


newcmap = ListedColormap([[11/255,45/255,94/255,1],[8/256,47/256,109/256,1],[7/256,57/256,125/256,1],
                          [9/256,66/256,142/256,1],[9/256,65/256,141/256,1],
                          [6/256,77/256,154/256,1],[9/256,87/256,162/256,1],[16/256,96/256,169/256,1],
                          [27/256,106/256,174/256,1],[36/256,115/256,182/256,1],[44/256,125/256,188/256,1],
                          [54/256,135/256,190/256,1],[64/256,144/256,196/256,1],[74/256,155/256,202/256,1],
                          [86/256,163/256,209/256,1],[101/256,169/256,212/256,1],[115/256,179/256,215/256,1],
                          [131/256,188/256,218/256,1],[146/256,196/256,221/256,1],[159/256,204/256,227/256,1],
                          [173/256,208/256,230/256,1],[185/256,213/256,234/256,1],[196/256,218/256,241/256,1],
                          [204/256,222/256,238/256,1],[210/256,228/256,244/256,1],[218/256,232/256,241/256,1],
                          [85/256,207/256,111/256,1],[166/256,224/256,139/256,1],[218/256,224/256,164/256,1],
                          [255/256,218/256,181/256,1],[247/256,208/256,149/256,1],[239/256,197/256,121/256,1],
                          [233/256,184/256,97/256,1],[223/256,175/256,64/256,1],[212/256,164/256,39/256,1],
                          [178/256,158/256,31/256,1],[166/256,150/256,29/256,1],[163/256,142/256,23/256,1],
                          [164/256,137/256,22/256,1],[162/256,132/256,18/256,1],[160/256,124/256,14/256,1],
                          [157/256,119/256,10/256,1],[155/256,112/256,7/256,1],[152/256,106/256,1/256,1],
                          [155/256,99/256,22/256,1],[160/256,90/256,78/256,1],[171/256,103/256,104/256,1],
                          [180/256,120/256,120/256,1],[181/256,139/256,140/256,1],[187/256,155/256,158/256,1],
                          [184/256,150/256,150/256,1],[191/256,169/256,169/256,1]])


def graficar_mapa_topografico(axe:Axes, topografia, lon_min: float, lon_max: float, lat_min: float, lat_max: float) -> None:
    """
    Descripción:
        Crea un mapa base geográfico usando Cartopy con proyección PlateCarree.
        Incluye líneas de costa, características geográficas (tierra, océano, fronteras,
        lagos y ríos) y etiquetas formateadas de coordenadas en los ejes.

    Parámetros:
        axe (cartopy.mpl.geoaxes.GeoAxesSubplot): Objeto axis de matplotlib con proyección Cartopy.
        topografia: Datos de topografía para graficar (viene de un archivo NetCDF con variables X, Y, Z).
        lon_min (float): Longitud mínima del área a mostrar (grados, oeste negativo).
        lon_max (float): Longitud máxima del área a mostrar (grados, oeste negativo).
        lat_min (float): Latitud mínima del área a mostrar (grados).
        lat_max (float): Latitud máxima del área a mostrar (grados).

    Retorna:
        None: Modifica el objeto Axes directamente agregando el mapa base y características.


    PENDIENTE
    """
    lon = topografia["lon"]
    lat = topografia["lat"]
    elevacion = topografia["elevacion"]
    
    axe.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    axe.pcolormesh(lon, lat, elevacion, cmap=newcmap, vmin=-4000, vmax=4000)
    axe.coastlines(resolution='10m')

    # Agregar ticks en los ejes X (longitud) e Y (latitud)
    xticks = list(range(int(lon_min), int(lon_max)+1, 2))
    yticks = list(range(int(lat_min), int(lat_max)+1, 2))
    axe.set_xticks(xticks, crs=ccrs.PlateCarree())
    axe.set_yticks(yticks, crs=ccrs.PlateCarree())

    # Formatear etiquetas de los ticks
    axe.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
    axe.yaxis.set_major_formatter(LATITUDE_FORMATTER)
