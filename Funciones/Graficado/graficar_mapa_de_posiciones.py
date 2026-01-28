import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import netCDF4 as nc


from Funciones.Utils.utils_get_config_vars import *
from Funciones.Utils.utilidades import *
from Funciones.Carga.cargar_datos_csv import leer_excel_de_despliegue_de_sondas 
from .base.Gra_mapa_cartopy import graficar_mapa_cartopy
from .base.Gra_batimetria_en_mapa import graficar_batimetria_en_mapa        
from .base.Gra_trayectorias_de_sonda import graficar_trayectorias_de_sonda
from .base.Gra_dar_formato_a_mapa import dar_formato_a_mapa

################################################################################

def graficar_mapa_con_posiciones(mostrar_figura: bool = False) -> None:
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
    
    tspan_column='tspan_rounded'
    origen_de_los_datos = get_origen_de_los_datos()
    
    
    ruta_a_la_carpeta_de_datos_procesados = crear_ruta_a_carpeta(get_carpeta_guardado_datos_procesados())
    nombre_del_archivo_de_datos_procesados = get_nombre_archivo_datos_procesados()
    ruta_de_archivo = os.path.join(ruta_a_la_carpeta_de_datos_procesados, nombre_del_archivo_de_datos_procesados)

    datos = cargar_diccionario_pickle(ruta_de_archivo)
    seriales_de_sondas = get_seriales_sondas()
    
    # Cargar datos de despliegue desde Excel
    df_excel_de_despliegue = leer_excel_de_despliegue_de_sondas(seriales_de_sondas)
    
    # Cargar datos de batimetría desde el archivo NetCDF
    datos_de_batimetria = cargar_datos_de_batimetria()
    
    # Recorrer cada sonda en el diccionario
    for serial in seriales_de_sondas:

        if serial not in datos:
            print(f"Advertencia: Serial {serial} no encontrado en los datos")
            continue
        
        # Datos de la sonda
        df_datos_de_la_sonda = datos[serial]
        
        # Obtener tspan (el eje X - en formato pd.DatetimeIndex)
        tspan = df_datos_de_la_sonda[tspan_column] if tspan_column else df_datos_de_la_sonda.index
            
        fig, ax = plt.subplots(figsize=(16, 7),
                               subplot_kw={'projection': ccrs.PlateCarree()})


        graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max)
        graficar_batimetria_en_mapa(ax, datos_de_batimetria = datos_de_batimetria)
        
        obj_mapeable = graficar_trayectorias_de_sonda(df_excel_de_despliegue, serial, df_datos_de_la_sonda) # devuelve el objeto mapeable para la colorbar
        
        
        # Preparar las propiedades del mapa (títulos, etiquetas, colorbar, etc.)
        t0str = tspan.min().strftime('%Y%m%d')
        tEstr = tspan.max().strftime('%Y%m%d')
        strDeFechas = str(f"{t0str}-{tEstr}")
        titulo = str(f"MAPA DE TRAYECTORIAS SONDA OCEANOGRÁFICA")
        subtitulo = str(f"NS-{serial}-{origen_de_los_datos}-{strDeFechas}")
        
        propieadades_de_mapa = {
            "obj_axes": ax, 
            "titulo": titulo, 
            "subtitulo": subtitulo, 
            "ylabel":'', 
            "xlabel": '', 
            "grid": True, 
            "obj_mapeable": obj_mapeable, 
            "colorbar_label": 'Rapidez de la corriente (m/s)', 
            "colorbar_min": get_escala_de_color_rapidez()["minimo"], 
            "colorbar_max": get_escala_de_color_rapidez()["maximo"], 
        }
        
        # Aplicar el formato al mapa con las propiedades definidas
        dar_formato_a_mapa(propieadades_de_mapa)
        
        # Mostrar y cerrar figura
        if mostrar_figura:
            plt.show()
        else:
            plt.close(fig)  # Cierra la figura para evitar que se muestre automáticamente

        # Guardar figura
        nombre_de_figura = (titulo + subtitulo).replace(" ", "_").replace("-", "_").replace("Á", "A")
        guardar_figura(figura=fig,
                       ruta_a_carpeta=crear_ruta_a_carpeta(get_carpeta_guardado_figuras()),
                       nombre_archivo= nombre_de_figura,
                       formato=get_formato_figuras(),
                       resolucion=get_resolucion_de_figuras())
        
        