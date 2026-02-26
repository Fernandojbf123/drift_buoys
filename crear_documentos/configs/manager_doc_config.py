import os
import dotenv
import importlib
import configs.configuracion_documentos
importlib.reload(configs.configuracion_documentos)

dotenv.load_dotenv()  # Carga las variables de entorno desde el archivo .env

def get_usar_NAS():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.usar_NAS

def get_ruta_al_excel_maestro():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_al_excel_de_despliegue_de_sondas
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_hoja_del_excel():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.hoja_del_excel

def get_ruta_a_carpeta_de_las_figuras():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_a_carpeta_de_las_figuras
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa


def get_ruta_a_carpeta_de_guardado_del_documento():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_a_carpeta_de_guardado_del_documento
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa


def get_nombre_de_la_plantilla_de_word():
    return configs.configuracion_documentos.nombre_de_la_plantilla_de_word
