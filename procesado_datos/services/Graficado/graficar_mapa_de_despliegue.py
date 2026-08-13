########################### IMPORTS NO TOCAR#####################################
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from procesado_datos.services.Utils.utilidades import *
from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig
from procesado_datos.services.Graficado.base.Gra_mapa_cartopy import graficar_mapa_cartopy
from procesado_datos.services.Graficado.base.Gra_mapa_topografia import graficar_mapa_topografico
from procesado_datos.services.Graficado.base.Gra_batimetria_en_mapa import graficar_batimetria_en_mapa        
from procesado_datos.services.Graficado.base.Gra_trayectorias_de_sonda import graficar_trayectorias_de_sonda
from procesado_datos.services.Graficado.base.Gra_dar_formato_a_figuras import *
from procesado_datos.services.Carga.cargar_datos_csv import leer_excel_de_despliegue_de_sondas

################################################################################

def graficar_mapa_de_despliegue(mostrar_figura: bool = False, ruta_a_la_carpeta_de_guardado: str = "", config: ProcesadoConfig | None = None) -> None:
    """
    Grafica un mapa de posiciones geográficas dentro de los límites dados.
    Utiliza la función graficar_mapa_cartopy para crear el mapa base.
    """
    
    ### 1. Cargar datos de archivo de configuración 
    seriales_a_analizar = config.seriales_de_sondas
    
    # Cargar datos de despliegue desde Excel maestro
    df_excel_de_despliegue = leer_excel_de_despliegue_de_sondas(config)
    df_excel_de_despliegue.dropna(subset=['serial_de_sonda'], inplace=True) # elimino ausentes o nulos para que la conversion no de error
    
    df_excel_de_despliegue['serial_de_sonda'] = df_excel_de_despliegue['serial_de_sonda'].astype(str) # Convertir a string
    puerto_de_salida = df_excel_de_despliegue[df_excel_de_despliegue["serial_de_sonda"] == seriales_a_analizar[0]]["lugar_de_salida"].values[-1] # Acá me interesa ir al excel de despliegue buscar el serial y conseguir el puerto de salida


    # Cargar sitios de embarque del excel maestro y obtener las coordenadas del puerto de salida
    sitios_de_embarque = pd.read_excel(config.ruta_al_excel_de_despliegue_de_sondas, sheet_name="sitios_de_embarque") 
    lon_pto = sitios_de_embarque.loc[sitios_de_embarque["nombre"] == puerto_de_salida, "longitud"].values[0] # Lon del puerto [o de los puertos]
    lat_pto = sitios_de_embarque.loc[sitios_de_embarque["nombre"] == puerto_de_salida, "latitud"].values[0] # Lat del puerto [o de los puertos]
        
    # Cargar coordenadas de despliegue de las sondas desde el excel maestro
    etiquetas = []
    lon_despliegues = []
    lat_despliegues = []
    
    for serial in seriales_a_analizar:
        idx = df_excel_de_despliegue[df_excel_de_despliegue["serial_de_sonda"] == serial].index[-1] # Busco el serial en el excel maestro
        if idx is not None:
            lon_despliegues.append(df_excel_de_despliegue.loc[idx,"longitud_maniobra"])
            lat_despliegues.append(df_excel_de_despliegue.loc[idx,"latitud_maniobra"])
            etiquetas.append(f"{serial}")
    
    # Crear array con todas las coordenadas de despliegue y el puerto de salida para ajustar el tamaño del mapa a la zona de interés
    longitudes = [] #Ruta que sigue el crucero
    latitudes = [] #Ruta que sigue el crucero
    longitudes.extend([lon_pto]) #le agrego el/los puertos de salida
    latitudes.extend([lat_pto]) #le agrego el/los puertos de salida
    
    longitudes.extend(lon_despliegues) #le agrego las coordenadas de despliegue de las sondas
    latitudes.extend(lat_despliegues) #le agrego las coordenadas de despl
    
    # Reajusto las coordenadas minimas y maximas del mapa para que se ajusten a los datos de despliegue y al puerto de salida, con un margen de 1 grado para mejor visualización
    lon_min = min(longitudes)-0.3
    lon_max = max(longitudes)+0.3
    lat_min = min(latitudes)-0.3
    lat_max = max(latitudes)+0.3
    
    # Cargar datos de batimetría desde el archivo NetCDF
    datos_de_batimetria = cargar_datos_de_batimetria(config)
    datos_de_topografia = cargar_datos_de_topografia(config)
    datos_de_topografia = recortar_datos_de_topografia_a_area_de_estudio(datos_de_topografia, lon_min, lon_max, lat_min, lat_max)
    datos_de_topografia = reemplazar_valores_de_topografia(datos_de_topografia, valor_a_reemplazar=-10, nuevo_valor=-10)
    
    # Graficar el mapa de despliegue con las coordenadas de las sondas
    fig, ax = plt.subplots(figsize=(16, 7),
                               subplot_kw={'projection': ccrs.PlateCarree()})
    
    graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max)
    graficar_mapa_topografico(axe=ax, topografia=datos_de_topografia, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
    graficar_batimetria_en_mapa(ax, datos_de_batimetria = datos_de_batimetria, config=config)
    
    
    # Graficar los puntos de despliegue en el mapa
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
    dar_formato_al_mapa(propieadades_de_mapa, config)
    ax.legend(loc='upper right', fontsize=config.tamanio_de_letra, frameon=True, edgecolor='black')
    
    # Mostrar y cerrar figura
    if mostrar_figura:
        plt.show()
    else:
        plt.close(fig)  # Cierra la figura para evitar que se muestre automáticamente

    # Guardar figura
    guardar_figura(figura=fig,
                    ruta_a_carpeta=ruta_a_la_carpeta_de_guardado,
                    nombre_archivo= dic_titulos["nombre_de_guardado"],
                    formato=config.formato_de_figuras,
                    resolucion=config.resolucion_de_figuras)
        
        