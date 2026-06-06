import os
import dotenv
import importlib
import configs.configuracion_documentos
importlib.reload(configs.configuracion_documentos)

dotenv.load_dotenv()  # Carga las variables de entorno desde el archivo .env

def get_orden_de_servicio():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.orden_de_servicio

def get_fecha_de_solicitud():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.fecha_de_solicitud

def ruta_al_excel_para_crear_documento():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_al_excel_para_crear_documento
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def hoja_del_excel_para_crear_documento():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.hoja_del_excel_para_crear_documeto

def get_ruta_a_carpeta_de_las_figuras(usar_NAS: bool = False):
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_a_carpeta_de_las_figuras
    if usar_NAS and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_ruta_a_carpeta_de_guardado_del_documento(usar_NAS: bool = False):
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_a_carpeta_de_guardado_del_documento
    if usar_NAS and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_ruta_al_excel_de_despliegue_de_sondas():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_al_excel_de_despliegue_de_sondas
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_hoja_del_excel_de_despliegue_de_sondas():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.hoja_del_excel_de_despliegue_de_sondas

def get_ruta_al_excel_de_campanias():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.rutal_al_excel_de_campanias
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_hoja_del_excel_de_campanias():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.hoja_del_excel_de_campanias

def get_usar_NAS():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.usar_NAS

def get_ruta_a_la_plantilla_de_word():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.ruta_a_la_plantilla_de_word

def get_ruta_a_la_plantilla_de_ppt():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.ruta_a_la_plantilla_de_ppt

def get_ruta_a_la_plantilla_de_pruebas():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.ruta_a_la_plantilla_de_pruebas

def get_ruta_a_carpeta_de_planes_de_crucero(usar_NAS: bool = False):
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_a_carpeta_de_planes_de_crucero
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_ruta_al_excel_de_porcentajes():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_al_excel_de_porcentajes
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa