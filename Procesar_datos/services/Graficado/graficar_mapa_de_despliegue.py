########################### IMPORTS NO TOCAR#####################################
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from configs.manager_configuracion import *
from services.Utils.utilidades import *
# from services.leer import leer_excel_maestro 
from .base.Gra_mapa_cartopy import graficar_mapa_cartopy
from .base.Gra_mapa_topografia import graficar_mapa_topografico
from .base.Gra_batimetria_en_mapa import graficar_batimetria_en_mapa        
from .base.Gra_trayectorias_de_sonda import graficar_trayectorias_de_sonda
from services.Graficado.base.Gra_dar_formato_a_figuras import *
################################################################################

def graficar_mapa_de_despliegue(mostrar_figura: bool = False) -> None:
    """
    Grafica un mapa de posiciones geográficas dentro de los límites dados.
    Utiliza la función graficar_mapa_cartopy para crear el mapa base.
    """
    
    ### 1. Cargar datos de archivo de configuración 
    seriales_a_analizar = get_seriales_sondas()
    coords_mapa = get_coordenadas_del_mapa()
    lon_min = coords_mapa["lon_min"]
    lon_max = coords_mapa["lon_max"]
    lat_min = coords_mapa["lat_min"]
    lat_max = coords_mapa["lat_max"]
    
    # Cargar datos de despliegue desde Excel maestro
    df_excel_de_despliegue = pd.read_excel(get_ruta_al_excel_de_despliegue_de_sondas(), sheet_name=get_nombre_de_la_hoja_con_informacion_de_sondas()) 
    df_excel_de_despliegue.dropna(subset=['serial_de_sonda'], inplace=True) # elimino ausentes o nulos para que la conversion no de error
    df_excel_de_despliegue['serial_de_sonda'] = df_excel_de_despliegue['serial_de_sonda'].astype(float).astype(int).astype(str)
    seriales_del_excel = df_excel_de_despliegue["serial_de_sonda"]
    puerto_de_salida = df_excel_de_despliegue[df_excel_de_despliegue["serial_de_sonda"] == seriales_a_analizar[0]]["lugar_de_salida"].values[-1] # Acá me interesa ir al excel de despliegue buscar el serial y conseguir el puerto de salida

    # Cargar datos de batimetría desde el archivo NetCDF
    datos_de_batimetria = cargar_datos_de_batimetria()
    datos_de_topografia = cargar_datos_de_topografia()
    datos_de_topografia = recortar_datos_de_topografia_a_area_de_estudio(datos_de_topografia, lon_min, lon_max, lat_min, lat_max)
    datos_de_topografia = reemplazar_valores_de_topografia(datos_de_topografia, valor_a_reemplazar=-10, nuevo_valor=-10)
    
    # Cargar sitios de embarque del excel maestro y obtener las coordenadas del puerto de salida
    sitios_de_embarque = pd.read_excel(get_ruta_al_excel_de_despliegue_de_sondas(), sheet_name="sitios_de_embarque") 
    lon_pto = sitios_de_embarque.loc[sitios_de_embarque["nombre"] == puerto_de_salida, "longitud"].values[0]
    lat_pto = sitios_de_embarque.loc[sitios_de_embarque["nombre"] == puerto_de_salida, "latitud"].values[0]
    
    # Preparar la ruta que sigue el crucero
    ruta_lon = [] #Ruta que sigue el crucero
    ruta_lat = [] #Ruta que sigue el crucero
    ruta_lon.append(lon_pto) #le agrego el puerto de salida
    ruta_lat.append(lat_pto) #le agrego el puerto de salida
    
    # Reajusto las coordenadas minimas y maximas del mapa para que se ajusten a los datos de despliegue y al puerto de salida, con un margen de 1 grado para mejor visualización
    lon_min = min(ruta_lon)-1.5
    lon_max = max(ruta_lon)+1.5
    lat_min = min(ruta_lat)-0.3
    lat_max = max(ruta_lat)+2
    
    fig, ax = plt.subplots(figsize=(16, 7),
                               subplot_kw={'projection': ccrs.PlateCarree()})
    
    graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max)
    graficar_mapa_topografico(axe=ax, topografia=datos_de_topografia, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
    graficar_batimetria_en_mapa(ax, datos_de_batimetria = datos_de_batimetria)
    
    etiquetas = []
    lon_despliegues = []
    lat_despliegues = []
    
    for serial in seriales_a_analizar:
        idx = df_excel_de_despliegue[df_excel_de_despliegue["serial_de_sonda"] == serial].index[-1] # Busco el serial en el excel maestro
        if idx is not None:
            lon_despliegues.append(df_excel_de_despliegue.loc[idx,"longitud_maniobra"])
            lat_despliegues.append(df_excel_de_despliegue.loc[idx,"latitud_maniobra"])
            etiquetas.append(f"{serial}")
    
    ruta_lon.extend(lon_despliegues)
    ruta_lat.extend(lat_despliegues)
    ruta_lon.append(lon_pto)
    ruta_lat.append(lat_pto)
    
    # ax.plot(ruta_lon, ruta_lat, linestyle='-', color='blue', marker='', linewidth=2, transform=ccrs.PlateCarree())
    # ax.plot(lon_despliegues, lat_despliegues, linestyle='', marker='o', markerfacecolor='red', markeredgecolor='black', markersize=8, transform=ccrs.PlateCarree())
    cmap = plt.cm.get_cmap('jet', len(seriales_a_analizar))
    for i, (lon, lat, serial) in enumerate(zip(lon_despliegues, lat_despliegues, seriales_a_analizar)):
        ax.scatter(
            lon,
            lat,
            marker='o',
            s=64,
            color=cmap(i),
            edgecolors='black',
            transform=ccrs.PlateCarree(),
            label=f"{serial}"
        )
        
    # Puerto de salida en naranja con borde
    # ax.plot(lon_pto,lat_pto, linestyle='', marker='o', markerfacecolor='orange', markeredgecolor="black", markersize=8, transform=ccrs.PlateCarree()) # punto de salida en naranja con borde
    
    # # Agregar etiquetas de texto al lado de cada coordenada de la ruta
    # lon_usada = np.array([])
    # lat_usada = np.array([])
    # for lon,lat, etiqueta in zip(lon_despliegues,lat_despliegues, etiquetas):
        
    #     differences = np.sqrt((lon_usada - lon)**2 + (lat_usada - lat)**2)
    #     cuenta = [ for dif in differences if dif < 0.07].count(True) # cuento cuantas coordenadas ya etiquetadas están cerca de la coordenada que quiero etiquetar
        
    #     delta = 0
    #     if cuenta != 0: # Si la coordenada está muy cerca de otra ya etiquetada, no la etiqueto para evitar amontonar etiquetas
    #         delta = cuenta * 0.07
                
    #     ax.text(lon + delta, 
    #             lat + delta, 
    #             etiqueta, 
    #             fontsize=get_tamanio_de_letra(),
    #             fontfamily=get_tipo_letra(),  
    #             color='black',
    #             fontweight='bold',
    #             transform=ccrs.PlateCarree())
    #     lon_usada = np.append(lon_usada, lon)
    #     lat_usada = np.append(lat_usada, lat)
        
        
    # Texto del puerto de salida
    # ax.text(lon_pto + 0.05, 
    #             lat_pto + 0.05, 
    #             puerto_de_salida, 
    #             fontsize=get_tamanio_de_letra(),
    #             fontfamily=get_tipo_letra(),  
    #             color='black',
    #             fontweight='bold',
    #             transform=ccrs.PlateCarree())
    
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
    ax.legend(loc='upper right', fontsize=get_tamanio_de_letra(), frameon=True, edgecolor='black')
    
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
        
        