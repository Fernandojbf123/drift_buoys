########################### IMPORTS NO TOCAR#####################################
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from Funciones.Utils.utils_get_config_vars import *
from Funciones.Utils.utilidades import *
from Funciones.Carga.cargar_datos_csv import leer_excel_de_despliegue_de_sondas_corregido 
from .base.Gra_mapa_cartopy import graficar_mapa_cartopy
from .base.Gra_mapa_topografia import graficar_mapa_topografico
from .base.Gra_batimetria_en_mapa import graficar_batimetria_en_mapa        
from .base.Gra_trayectorias_de_sonda import graficar_trayectorias_de_sonda
from Funciones.Graficado.base.Gra_dar_formato_a_figuras import *
################################################################################

def graficar_mapa_de_despliegue(mostrar_figura: bool = False) -> None:
    """
    Grafica un mapa de posiciones geográficas dentro de los límites dados.
    Utiliza la función graficar_mapa_cartopy para crear el mapa base.
    """
        # Esto se carga desde el archivo de configuración
    coords_mapa = get_coordenadas_del_mapa()
    lon_min = coords_mapa["lon_min"]
    lon_max = coords_mapa["lon_max"]
    lat_min = coords_mapa["lat_min"]
    lat_max = coords_mapa["lat_max"]
    
    # Cargar datos de despliegue desde Excel
    df_excel_de_despliegue = leer_excel_de_despliegue_de_sondas_corregido()
    
    # Cargar datos de batimetría desde el archivo NetCDF
    datos_de_batimetria = cargar_datos_de_batimetria()
    datos_de_topografia = cargar_datos_de_topografia()
    datos_de_topografia = recortar_datos_de_topografia_a_area_de_estudio(datos_de_topografia, lon_min, lon_max, lat_min, lat_max)
    datos_de_topografia = reemplazar_valores_de_topografia(datos_de_topografia, valor_a_reemplazar=-10, nuevo_valor=-10)
    
    seriales_a_analizar = get_seriales_sondas()
    
    seriales_del_excel = df_excel_de_despliegue["serie_de_sonda"]
    lon = df_excel_de_despliegue["longitud_corregida"].dropna()
    lat = df_excel_de_despliegue["latitud_corregida"].dropna()
    
    # Obtener lat lon del puerto de salida
    puertos = get_puertos() # todos los puertos de la base de datos
    puerto_de_salida = get_puerto_de_salida()
    lon_pto = puertos[puerto_de_salida]["lon"]
    lat_pto = puertos[puerto_de_salida]["lat"]
    
    ruta_lon = [] #Ruta que sigue el crucero
    ruta_lat = [] #Ruta que sigue el crucero
    ruta_lon.append(lon_pto) #le agrego el puerto de salida
    ruta_lat.append(lat_pto) #le agrego el puerto de salida
    
    # Reajusto las coordenadas minimas y maximas del mapa para que se ajusten a los datos de despliegue y al puerto de salida, con un margen de 1 grado para mejor visualización
    lon_min = min(ruta_lon)-1.5
    lon_max = max(ruta_lon)+1.5
    lat_min = min(ruta_lat)-.3
    lat_max = max(ruta_lat)+2
    
    fig, ax = plt.subplots(figsize=(16, 7),
                               subplot_kw={'projection': ccrs.PlateCarree()})
    
    graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max)
    graficar_mapa_topografico(axe=ax, topografia=datos_de_topografia, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
    graficar_batimetria_en_mapa(ax, datos_de_batimetria = datos_de_batimetria)
    
    etiquetas = []
    lon_despliegues = []
    lat_despliegues = []
    for (lon,lat, serial) in zip(lon,lat, seriales_del_excel):
        if serial not in seriales_a_analizar:
            continue
        etiquetas.append(f"{serial}")
        lon_despliegues.append(lon)
        lat_despliegues.append(lat) 
    
    ruta_lon.extend(lon_despliegues)
    ruta_lat.extend(lat_despliegues)
    ruta_lon.append(lon_pto)
    ruta_lat.append(lat_pto)
    
    ax.plot(ruta_lon, ruta_lat, linestyle='-', color='blue', marker='', linewidth=2, transform=ccrs.PlateCarree())
    ax.plot(lon_despliegues, lat_despliegues, linestyle='', marker='o', markerfacecolor='red', markeredgecolor='blue', markersize=8, transform=ccrs.PlateCarree())
    ax.plot(lon_pto,lat_pto, linestyle='', marker='o', markerfacecolor='orange', markeredgecolor="blue", markersize=8, transform=ccrs.PlateCarree()) # punto de salida en naranja con borde
    
    # Agregar etiquetas de texto al lado de cada coordenada de la ruta
    for lon,lat, etiqueta in zip(lon_despliegues,lat_despliegues, etiquetas):
        ax.text(lon + 0.05, 
                lat + 0.05, 
                etiqueta, 
                fontsize=get_tamanio_de_letra(),
                fontfamily=get_tipo_letra(),  
                color='black',
                fontweight='bold',
                transform=ccrs.PlateCarree())
    
    ax.text(lon_pto + 0.05, 
                lat_pto + 0.05, 
                get_puerto_de_salida(), 
                fontsize=get_tamanio_de_letra(),
                fontfamily=get_tipo_letra(),  
                color='black',
                fontweight='bold',
                transform=ccrs.PlateCarree())
    
    dic_titulos = {"titulo": "Coordenadas de despliegue", "subtitulo": "", "nombre_de_guardado": "mapa_de_despliegue"}
                
    # Preparar las propiedades del mapa (títulos, etiquetas, colorbar, etc.)
    propieadades_de_mapa = {
        "obj_axes": ax, 
        "titulo": dic_titulos["titulo"], 
        "subtitulo": dic_titulos["subtitulo"], 
        "ylabel":'', 
        "xlabel": '', 
        "grid": True, 
        "obj_mapeable": None, 
        "colorbar_label": '', 
        "colorbar_min": None, 
        "colorbar_max": None, 
    }
        
    # # Aplicar el formato al mapa con las propiedades definidas
    dar_formato_al_mapa(propieadades_de_mapa)
        
    # Mostrar y cerrar figura
    if mostrar_figura:
        plt.show()
    else:
        plt.close(fig)  # Cierra la figura para evitar que se muestre automáticamente

    # Guardar figura
    guardar_figura(figura=fig,
                    ruta_a_carpeta=crear_ruta_a_carpeta(get_carpeta_guardado_figuras()),
                    nombre_archivo= dic_titulos["nombre_de_guardado"],
                    formato=get_formato_figuras(),
                    resolucion=get_resolucion_de_figuras())
        
        