#################### FUNCIONES DE ACCESO A CONFIGURACIÓN ####################
import pandas as pd
import Configs.configuracion_general

def _get_config_value(key):
    """Obtiene un valor de la configuración general de forma dinámica"""
    import importlib
    importlib.reload(Configs.configuracion_general)
    return Configs.configuracion_general.general_config[key]

def get_fecha_de_inicio_del_analisis():
     fecha = _get_config_value("fecha_de_inicio_del_analisis")
     fecha = pd.to_datetime(fecha, format="%Y-%m-%d %H:%M:%S")
     return fecha

def get_fecha_de_fin_del_analisis():
     fecha = _get_config_value("fecha_de_fin_del_analisis")
     fecha = pd.to_datetime(fecha, format="%Y-%m-%d %H:%M:%S")
     return fecha

def get_delta_tiempo():
    return _get_config_value("delta_tiempo")

def get_ruta_al_excel_de_despliegue_de_sondas():
    return _get_config_value("ruta_al_excel_de_despliegue_de_sondas")

def get_carpeta_datos_crudos():
    return _get_config_value("carpeta_de_datos_crudos")

def get_carpeta_guardado_datos_procesados():
    return _get_config_value("carpeta_de_guardado_de_datos_procesados")

def get_nombre_archivo_datos_procesados():
    return _get_config_value("nombre_del_archivo_de_datos_procesados")

def get_nombre_del_archivo_de_datos_previos_a_la_fecha_de_estudio():
    return _get_config_value("nombre_del_archivo_de_datos_previos_a_la_fecha_de_estudio")

def get_nombre_del_excel_de_porcentajes():
    return _get_config_value("nombre_del_excel_de_porcentajes")

def get_carpeta_guardado_figuras():
    return _get_config_value("carpeta_de_guardado_de_figuras")

def get_resolucion_de_figuras():
    return _get_config_value("resolucion_de_figuras")

def get_seriales_sondas():
    return _get_config_value("seriales_de_sondas")

def get_delta_tiempo():
    return _get_config_value("delta_tiempo")

def get_formato_figuras():
    return _get_config_value("formato_de_figuras")

def get_resolucion_figuras():
    return _get_config_value("resolucion_de_figuras")

def get_origen_de_los_datos():
    return _get_config_value("origen_de_los_datos")

def get_decimales_figuras():
    return _get_config_value("decimales_en_figuras")

def get_tipo_letra():
    return _get_config_value("tipo_de_letra")

def get_tamanio_de_letra():
    return _get_config_value("tamanio_de_letra")

def get_numero_bins_histograma():
    return _get_config_value("numero_de_bins_histograma")

def get_variables_graficar():
    return _get_config_value("variables_a_graficar")

def get_coordenadas_del_mapa():
    return _get_config_value("coordenadas_del_mapa")

def get_escala_de_color_rapidez():
    return _get_config_value("escala_de_color_rapidez")

def get_ruta_a_datos_batimetria():
    return _get_config_value("ruta_a_datos_batimetria")

def get_curvas_de_batimetria():
    curvas = _get_config_value("curvas_de_batimetria")
    return sorted(curvas)

def get_graficar_trayectorias_pasadas():
    return _get_config_value("graficar_trayectorias_pasadas")

def get_ruta_a_datos_topografia():
    return _get_config_value("ruta_a_datos_topografia")

def get_puerto_de_salida():
    return _get_config_value("puerto_de_salida")