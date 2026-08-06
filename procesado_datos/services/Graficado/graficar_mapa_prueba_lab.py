########################### IMPORTS NO TOCAR#####################################
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig

from procesado_datos.services.Utils.utilidades import (cargar_datos_de_batimetria, 
                                                       cargar_datos_de_topografia, 
                                                       recortar_datos_de_topografia_a_area_de_estudio, 
                                                       reemplazar_valores_de_topografia)

from procesado_datos.services.Graficado.base.Gra_mapa_cartopy import graficar_mapa_cartopy
from procesado_datos.services.Graficado.base.Gra_mapa_topografia import graficar_mapa_topografico
from procesado_datos.services.Graficado.base.Gra_batimetria_en_mapa import graficar_batimetria_en_mapa        
from procesado_datos.services.Graficado.base.Gra_trayectorias_de_sonda import graficar_trayectorias_de_sonda

from procesado_datos.services.Graficado.base.Gra_dar_formato_a_figuras import *
from procesado_datos.services.Utils.utilidades import *

################################################################################

def graficar_mapa_prueba_lab(datos, mostrar_figura: bool = False, ruta_a_la_carpeta_de_guardado ="", config: ProcesadoConfig | None = None) -> None:
    """
    Grafica un mapa de posiciones geográficas dentro de los límites dados.
    Utiliza la función graficar_mapa_cartopy para crear el mapa base.
    """
    
    ### 1. Cargar datos de archivo de configuración 
    lon_min = config.coordenadas_del_mapa_pruebas_lab["lon_min"]
    lon_max = config.coordenadas_del_mapa_pruebas_lab["lon_max"]
    lat_min = config.coordenadas_del_mapa_pruebas_lab["lat_min"]
    lat_max = config.coordenadas_del_mapa_pruebas_lab["lat_max"]
    

    # Cargar datos de batimetría desde el archivo NetCDF
    datos_de_batimetria = cargar_datos_de_batimetria(config)
    datos_de_topografia = cargar_datos_de_topografia(config)
    datos_de_topografia = recortar_datos_de_topografia_a_area_de_estudio(datos_de_topografia, lon_min, lon_max, lat_min, lat_max)
    datos_de_topografia = reemplazar_valores_de_topografia(datos_de_topografia, valor_a_reemplazar=-10, nuevo_valor=-10)
    
    serial = list(datos.keys())[0] # Obtener el primer serial de sonda del diccionario de datos
    
    df = datos[serial]
    lat_boya = df["latitud"].iloc[0]
    lon_boya = df["logitud"].iloc[0]

    fig, ax = plt.subplots(figsize=(16, 7),
                            subplot_kw={'projection': ccrs.PlateCarree()})

    graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max)
    graficar_mapa_topografico(axe=ax, topografia=datos_de_topografia, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
    graficar_batimetria_en_mapa(axe = ax, datos_de_batimetria = datos_de_batimetria, config = config)
    
    ax.plot(lon_boya, lat_boya, linestyle='', marker='o', markerfacecolor='red', markeredgecolor='black', markersize=8, transform=ccrs.PlateCarree())
    
    dic_titulos = {"titulo": "MAPA DE UBICACIÓN DE SONDA DURANTE PRUEBAS DE LABORATORIO", "subtitulo": "", "nombre_de_guardado": "mapa_de_prueba_lab"}
                
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
    dar_formato_al_mapa(propieadades_de_mapa, config)
    ax.set_xticks(np.arange(lon_min, lon_max+1, 1))  # Eliminar ticks del eje y
    ax.set_yticks(np.arange(lat_min, lat_max+1, 1))  # Eliminar ticks del eje x
        
    # Mostrar y cerrar figura
    if mostrar_figura:
        plt.show()
    else:
        plt.close(fig)  # Cierra la figura para evitar que se muestre automáticamente

    # Guardar figura
    guardar_figura(
        figura=fig,
        ruta_a_carpeta=ruta_a_la_carpeta_de_guardado,
        nombre_archivo= dic_titulos["nombre_de_guardado"],
        formato=config.formato_de_figuras,
        resolucion=config.resolucion_de_figuras)
    
        