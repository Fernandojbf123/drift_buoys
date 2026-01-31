########################### IMPORTS NO TOCAR#####################################
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from Funciones.Utils.utils_get_config_vars import *
from Funciones.Utils.utilidades import *
from Funciones.Carga.cargar_datos_csv import leer_excel_de_despliegue_de_sondas 
from .base.Gra_mapa_cartopy import graficar_mapa_cartopy
from .base.Gra_batimetria_en_mapa import graficar_batimetria_en_mapa        
from .base.Gra_trayectorias_de_sonda import graficar_trayectorias_de_sonda
from Funciones.Graficado.base.Gra_dar_formato_a_figuras import *
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
    ruta_al_archivo_de_datos_previos_a_la_fecha_de_estudio = os.path.join(ruta_a_la_carpeta_de_datos_procesados, get_nombre_del_archivo_de_datos_previos_a_la_fecha_de_estudio())

    datos = cargar_diccionario_pickle(ruta_de_archivo) # Son los datos del periodo de vigencia
    datos_previos_a_la_fecha_de_estudio = cargar_diccionario_pickle(ruta_al_archivo_de_datos_previos_a_la_fecha_de_estudio) # Son los datos previos a la fecha de estudio
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
        df_datos_previos_de_la_sonda = datos_previos_a_la_fecha_de_estudio.get(serial,None)
        
        # Obtener tspan (el eje X - en formato pd.DatetimeIndex)
        tspan = df_datos_de_la_sonda[tspan_column] if tspan_column else df_datos_de_la_sonda.index
            
        fig, ax = plt.subplots(figsize=(16, 7),
                               subplot_kw={'projection': ccrs.PlateCarree()})


        graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max)
        graficar_batimetria_en_mapa(ax, datos_de_batimetria = datos_de_batimetria)
        
        obj_mapeable = graficar_trayectorias_de_sonda(df_excel_de_despliegue = df_excel_de_despliegue, 
                                                      serial = serial, 
                                                      df_datos_de_la_sonda = df_datos_de_la_sonda, 
                                                      df_datos_previos_de_la_sonda = df_datos_previos_de_la_sonda,
                                                      graficar_trayectorias_pasadas = get_graficar_trayectorias_pasadas()) # devuelve el objeto mapeable para la colorbar
        
        dic_titulos = crear_titulos_de_mapa_y_nombre_de_guardado(tspan = tspan, NS_sonda= serial)
                
        # Preparar las propiedades del mapa (títulos, etiquetas, colorbar, etc.)
        propieadades_de_mapa = {
            "obj_axes": ax, 
            "titulo": dic_titulos["titulo"], 
            "subtitulo": dic_titulos["subtitulo"], 
            "ylabel":'', 
            "xlabel": '', 
            "grid": True, 
            "obj_mapeable": obj_mapeable, 
            "colorbar_label": 'Rapidez de la corriente (m/s)', 
            "colorbar_min": get_escala_de_color_rapidez()["minimo"], 
            "colorbar_max": get_escala_de_color_rapidez()["maximo"], 
        }
        
        # Aplicar el formato al mapa con las propiedades definidas
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
        
        