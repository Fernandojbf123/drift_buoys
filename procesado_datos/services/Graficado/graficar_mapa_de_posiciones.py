########################### IMPORTS NO TOCAR#####################################
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from procesado_datos.services.Utils.utilidades import *
from procesado_datos.services.Carga.cargar_datos_csv import *
from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig
from procesado_datos.services.Graficado.base.Gra_mapa_cartopy import graficar_mapa_cartopy
from procesado_datos.services.Graficado.base.Gra_mapa_topografia import graficar_mapa_topografico
from procesado_datos.services.Graficado.base.Gra_batimetria_en_mapa import graficar_batimetria_en_mapa        
from procesado_datos.services.Graficado.base.Gra_trayectorias_de_sonda import graficar_trayectorias_de_sonda
from procesado_datos.services.Graficado.base.Gra_dar_formato_a_figuras import *
################################################################################

def graficar_mapa_de_posiciones(datos: dict, 
                                ruta_a_la_carpeta_de_guardado: str, 
                                mostrar_figura: bool = False, 
                                config: ProcesadoConfig | None = None) -> None:
    """
    Grafica un mapa de posiciones geográficas dentro de los límites dados.
    Utiliza la función graficar_mapa_cartopy para crear el mapa base.
    """
    # Esto se carga desde el archivo de configuración
    coords_mapa = config.coordenadas_del_mapa
    lon_min = coords_mapa["lon_min"]
    lon_max = coords_mapa["lon_max"]
    lat_min = coords_mapa["lat_min"]
    lat_max = coords_mapa["lat_max"]
    
    tspan_column='tspan_rounded'
    
    seriales_de_sondas = config.seriales_de_sondas
    
    # Cargar datos de despliegue desde Excel
    df_excel_de_despliegue = leer_excel_de_despliegue_de_sondas(config)
    
    # Cargar datos de batimetría desde el archivo NetCDF
    datos_de_batimetria = cargar_datos_de_batimetria(config)
    datos_de_topografia = cargar_datos_de_topografia(config)
    datos_de_topografia = recortar_datos_de_topografia_a_area_de_estudio(datos_de_topografia, lon_min, lon_max, lat_min, lat_max)
    datos_de_topografia = reemplazar_valores_de_topografia(datos_de_topografia, valor_a_reemplazar=-10, nuevo_valor=-10)
    
    # Recorrer cada sonda en el diccionario
    for serial in seriales_de_sondas:

        if serial not in datos:
            print(f"Advertencia: Serial {serial} no encontrado en los datos")
            continue
        
        # Datos de la sonda
        df_datos_de_la_sonda = datos[serial]
        
        df_datos_previos_de_la_sonda = None
        
        # Obtener tspan (el eje X - en formato pd.DatetimeIndex)
        tspan = df_datos_de_la_sonda[tspan_column] if tspan_column else df_datos_de_la_sonda.index
            
        fig, ax = plt.subplots(figsize=(16, 7),
                               subplot_kw={'projection': ccrs.PlateCarree()})


        graficar_mapa_cartopy(ax, lon_min, lon_max, lat_min, lat_max)
        graficar_mapa_topografico(axe=ax, topografia=datos_de_topografia, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
        graficar_batimetria_en_mapa(ax, datos_de_batimetria = datos_de_batimetria, config=config)
        
        obj_mapeable = graficar_trayectorias_de_sonda(
            df_excel_de_despliegue = df_excel_de_despliegue, 
            serial = serial, 
            df_datos_de_la_sonda = df_datos_de_la_sonda, 
        ) # devuelve el objeto mapeable para la colorbar
    
        dic_titulos = crear_titulos_de_mapa_y_nombre_de_guardado(tspan = tspan, NS_sonda= serial, config=config)
                
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
            "colorbar_min": config.escala_de_color_rapidez["minimo"], 
            "colorbar_max": config.escala_de_color_rapidez["maximo"], 
        }
        
        # Aplicar el formato al mapa con las propiedades definidas
        dar_formato_al_mapa(propieadades_de_mapa, config)
        
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
            resolucion=config.resolucion_de_figuras
        )
        
        