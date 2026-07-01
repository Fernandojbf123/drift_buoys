import configs.configuracion_general as config

def _get_config_value(variable_name):
    """Obtiene un valor de la configuración general de forma dinámica"""
    import importlib
    importlib.reload(config)
    
    return getattr(config, variable_name)

def get_seriales_sondas():
    return _get_config_value("seriales_de_sondas")

def get_carpeta_de_datos_crudos():
    return _get_config_value("carpeta_de_datos_crudos")