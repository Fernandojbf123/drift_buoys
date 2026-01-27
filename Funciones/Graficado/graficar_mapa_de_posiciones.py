import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import cartopy.crs as ccrs
from .base.Gra_mapa_cartopy import graficar_mapa_cartopy
from Funciones.Utils.utils_get_config_vars import *
from Funciones.Utils.utilidades import *
from Funciones.Carga.cargar_datos_csv import leer_excel_de_despliegue_de_sondas 

################################################################################

def graficar_mapa_con_posiciones():
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
    tipo_de_letra = get_tipo_letra()
    tamanio_de_letra = get_tamanio_letra()
    titlesize = tamanio_de_letra + 6
    
    ruta_a_la_carpeta_de_datos_procesados = crear_ruta_a_carpeta(get_carpeta_guardado_datos_procesados())
    nombre_del_archivo_de_datos_procesados = get_nombre_archivo_datos_procesados()
    ruta_de_archivo = os.path.join(ruta_a_la_carpeta_de_datos_procesados, nombre_del_archivo_de_datos_procesados)

    datos = cargar_diccionario_pickle(ruta_de_archivo)
    seriales_de_sondas = get_seriales_sondas()
    
    # Cargar datos de despliegue desde Excel
    df_excel_de_despliegue = leer_excel_de_despliegue_de_sondas(seriales_de_sondas)
    
    # Recorrer cada sonda en el diccionario
    for serial in seriales_de_sondas:

        if serial not in datos:
            print(f"Advertencia: Serial {serial} no encontrado en los datos")
            continue
        
        # Obtener posiciones iniciales del excel de despliegue
        lat_ini_series = df_excel_de_despliegue[df_excel_de_despliegue['serie_de_sonda'] == serial]['latitud_de_despliegue']
        lon_ini_series = df_excel_de_despliegue[df_excel_de_despliegue['serie_de_sonda'] == serial]['longitud_de_despliegue']
        lat_ini = float(lat_ini_series.iloc[0]) if not lat_ini_series.empty else None
        lon_ini = -float(lon_ini_series.iloc[0]) if not lon_ini_series.empty else None
        
        # Obtener posiciones y rapidez de corriente del diccionario de datos
        df = datos[serial]
        latitud = df['latitud']
        longitud = df['longitud']   
        rap_corriente = df['rap_corriente']
        lat_fin = latitud.iloc[-1]
        lon_fin = longitud.iloc[-1]
        
         # Obtener tspan (el eje X - en formato pd.DatetimeIndex)
        tspan = df[tspan_column] if tspan_column else df.index
        
        cmap = LinearSegmentedColormap.from_list("azul_rojo", ["blue", "red"])
    
        fig, ax = plt.subplots(figsize=(16, 7),
                               subplot_kw={'projection': ccrs.PlateCarree()})

        graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max)
        sc = plt.scatter(longitud, latitud, c=rap_corriente, cmap=cmap, s=10, vmin=0, vmax=1.5, transform=ccrs.PlateCarree())
        plt.colorbar(sc, label='Rapidez de la corriente (m/s)', orientation='vertical', pad=0.02, aspect=30)
        plt.scatter([lon_ini], [lat_ini], c='yellow', edgecolors='black', linewidths=2, s=50, transform=ccrs.PlateCarree())
        plt.scatter([lon_fin], [lat_fin], c='red', edgecolors='black', linewidths=2, s=50, transform=ccrs.PlateCarree())
        
        
        ## Estética del gráfico
        # Preparar el título de la figura y de guardado
        t0str = tspan.min().strftime('%Y%m%d')
        tEstr = tspan.max().strftime('%Y%m%d')
        strDeFechas = str(f"{t0str}-{tEstr}")
        tituloBase = str(f"MAPA-DE-TRAYECTORIAS-SONDA-OCEANOGRÁFICA-NS-{serial}-{origen_de_los_datos}-{strDeFechas}")
        
        plt.grid(True, which='both', linestyle='--', color='gray', alpha=0.5)        
        plt.title(tituloBase, font=tipo_de_letra, fontweight='bold', fontsize=titlesize)
        nombre_de_figura = tituloBase.replace(" ", "_").replace("-", "_").replace("Á", "A")

        # Ajustar layout
        plt.tight_layout()
        # plt.show()  # mostrar la figura en el notebook
        plt.close(fig)  # Cierra la figura para evitar que se muestre automáticamente

        # Guardar figura
        guardar_figura(figura=fig,
                       ruta_a_carpeta=crear_ruta_a_carpeta(
                           get_carpeta_guardado_figuras()),
                       nombre_archivo=nombre_de_figura,
                       formato=get_formato_figuras(),
                       resolucion=get_resolucion_de_figuras())
        
        