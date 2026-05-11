########################### IMPORTS NO TOCAR#####################################
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from configs.manager_configuracion import *
from services.Utils.utilidades import *
from .base.Gra_mapa_cartopy import graficar_mapa_cartopy
from .base.Gra_mapa_topografia import graficar_mapa_topografico
from .base.Gra_batimetria_en_mapa import graficar_batimetria_en_mapa        
from .base.Gra_trayectorias_de_sonda import graficar_trayectorias_de_sonda
from services.Graficado.base.Gra_dar_formato_a_figuras import *
################################################################################

def graficar_mapa_prueba_lab(mostrar_figura: bool = False) -> None:
    """
    Grafica un mapa de posiciones geográficas dentro de los límites dados.
    Utiliza la función graficar_mapa_cartopy para crear el mapa base.
    """
    
    # Cargar datos procesados
    ruta_a_la_carpeta_de_datos_procesados = crear_ruta_a_carpeta(get_carpeta_guardado_datos_procesados())
    nombre_del_archivo_de_datos_procesados = "datos_interpolados"#get_nombre_archivo_datos_procesados()
    ruta_de_archivo = os.path.join(ruta_a_la_carpeta_de_datos_procesados, nombre_del_archivo_de_datos_procesados)

    datos = cargar_diccionario_pickle(ruta_de_archivo)
    serial = list(datos.keys())[0]
    lat_boya = datos[serial]["latitud"][0]
    lon_boya = datos[serial]["longitud"][0]

    seriales_de_sondas = get_seriales_sondas()
    # Recorrer cada sonda en el diccionario
    
    ### 1. Cargar datos de archivo de configuración 
    lon_min = -94
    lon_max = -90
    lat_min = 18
    lat_max = 21
    
    # Cargar datos de despliegue desde Excel maestro
    df_excel_de_despliegue = pd.read_excel(get_ruta_al_excel_de_despliegue_de_sondas(), sheet_name=get_nombre_de_la_hoja_con_informacion_de_sondas()) 
    df_excel_de_despliegue.dropna(subset=['serial_de_sonda'], inplace=True) # elimino ausentes o nulos para que la conversion no de error
    df_excel_de_despliegue['serial_de_sonda'] = df_excel_de_despliegue['serial_de_sonda'].astype(float).astype(int).astype(str)

    # Cargar datos de batimetría desde el archivo NetCDF
    datos_de_batimetria = cargar_datos_de_batimetria()
    datos_de_topografia = cargar_datos_de_topografia()
    datos_de_topografia = recortar_datos_de_topografia_a_area_de_estudio(datos_de_topografia, lon_min, lon_max, lat_min, lat_max)
    datos_de_topografia = reemplazar_valores_de_topografia(datos_de_topografia, valor_a_reemplazar=-10, nuevo_valor=-10)
    
    
    fig, ax = plt.subplots(figsize=(16, 7),
                               subplot_kw={'projection': ccrs.PlateCarree()})
    
    graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max)
    graficar_mapa_topografico(axe=ax, topografia=datos_de_topografia, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
    graficar_batimetria_en_mapa(ax, datos_de_batimetria = datos_de_batimetria)
    
    ax.plot(lon_boya, lat_boya, linestyle='', marker='o', markerfacecolor='red', markeredgecolor='black', markersize=8, transform=ccrs.PlateCarree())
    
    dic_titulos = {"titulo": "Mapa de ubicación de sonda durante pruebas de laboratorio", "subtitulo": "", "nombre_de_guardado": "mapa_de_prueba_lab"}
                
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
    ax.set_xticks(np.arange(-94, -89, 1))  # Eliminar ticks del eje y
    ax.set_yticks(np.arange(18, 22, 1))  # Eliminar ticks del eje x
        
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
        
        