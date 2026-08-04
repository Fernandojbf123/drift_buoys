import os
import re
import dotenv
import importlib
import configs.configuracion_documentos
import services
importlib.reload(configs.configuracion_documentos)

dotenv.load_dotenv()  # Carga las variables de entorno desde el archivo .env

def validate_config_value(attr_name: str, expect_type: type | tuple | None = None, must_exist_path: bool = False, allow_empty: bool = False) -> tuple[bool, str]:
    """Valida una variable en `configs.configuracion_documentos`.

    Retorna `(True, "")` si pasa, o `(False, mensaje_de_error)` si falla.
    """
    errors: list[str] = []
    try:
        value = getattr(configs.configuracion_documentos, attr_name)
    except AttributeError:
        return False, f"Falta la variable de configuración: {attr_name}"

    if expect_type is not None and not isinstance(value, expect_type):
        errors.append(f"Tipo inválido para '{attr_name}' (esperado {expect_type}, obtenido {type(value)})")

    if not allow_empty and isinstance(value, str) and value.strip() == "":
        errors.append(f"Variable '{attr_name}' está vacía")

    if must_exist_path and isinstance(value, str):
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        if get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, value)
        else:
            ruta_completa = value
        if not os.path.exists(ruta_completa):
            errors.append(f"Ruta no existe para '{attr_name}': {ruta_completa}")

    if errors:
        return False, "; ".join(errors)
    return True, ""

def ruta_al_excel_para_crear_documento():
    """Obtiene un valor de la configuración general de forma dinámica"""
    # Validar configuración
    if not validate_config_value("ruta_al_excel_para_crear_documento", expect_type=str, must_exist_path=True, allow_empty=False):
        return None
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = services.doc101.configuracion_101.ruta_al_excel_para_crear_documento
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def hoja_del_excel_para_crear_documento():
    """Obtiene un valor de la configuración general de forma dinámica"""
    if not validate_config_value("hoja_del_excel_para_crear_documeto", expect_type=str, allow_empty=False):
        return None
    return services.doc101.configuracion_101

def get_ruta_a_carpeta_de_las_figuras(usar_NAS: bool = False):

    if not validate_config_value(
        "ruta_a_carpeta_de_las_figuras",
        expect_type=str,
        allow_empty=False,
    ):
        return None

    carpeta = services.doc101.configuracion_101.ruta_a_carpeta_de_las_figuras

    # Obtiene 202606
    hoja = hoja_del_excel_para_crear_documento()

    ruta_relativa = os.path.join(
        carpeta,
        hoja,
        "documento",
    )

    ruta_al_NAS = os.getenv("ruta_al_NAS")

    if usar_NAS and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, ruta_relativa)
    else:
        ruta_completa = ruta_relativa

    return ruta_completa


def get_ruta_a_carpeta_de_guardado_del_documento(usar_NAS: bool = False):

    if not validate_config_value(
        "ruta_a_carpeta_de_guardado_del_documento",
        expect_type=str,
        allow_empty=False,
    ):
        return None

    carpeta = services.doc101.configuracion_101.ruta_a_carpeta_de_guardado_del_documento

    # Obtiene 202606
    hoja = hoja_del_excel_para_crear_documento()

    ruta_relativa = os.path.join(
        carpeta,
        hoja,
        "documento",
    )

    ruta_al_NAS = os.getenv("ruta_al_NAS")

    if usar_NAS and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, ruta_relativa)
    else:
        ruta_completa = ruta_relativa

    return ruta_completa

def get_ruta_al_excel_de_despliegue_de_sondas():
    """Obtiene un valor de la configuración general de forma dinámica"""
    if not validate_config_value("ruta_al_excel_de_despliegue_de_sondas", expect_type=str, must_exist_path=True, allow_empty=False):
        return None
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = services.doc101.configuracion_101.ruta_al_excel_de_despliegue_de_sondas
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_hoja_del_excel_de_despliegue_de_sondas():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return services.doc101.configuracion_101.hoja_del_excel_de_despliegue_de_sondas

def get_ruta_al_excel_de_campanias():
    """Obtiene un valor de la configuración general de forma dinámica"""
    if not validate_config_value("rutal_al_excel_de_campanias", expect_type=str, must_exist_path=True, allow_empty=False):
        return None
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = services.doc101.configuracion_101.rutal_al_excel_de_campanias
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_hoja_del_excel_de_campanias():
    """Obtiene un valor de la configuración general de forma dinámica"""
    if not validate_config_value("hoja_del_excel_de_campanias", expect_type=str, allow_empty=False):
        return None
    return services.doc101.configuracion_101.hoja_del_excel_de_campanias

def get_usar_NAS():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return services.doc101.configuracion_101.usar_NAS

def get_ruta_a_la_plantilla_de_word():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ok, error_message = validate_config_value(
        "ruta_a_la_plantilla_de_word",
        expect_type=str,
        must_exist_path=True,
        allow_empty=False,
    )
    if not ok:
        return None

    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = services.doc101.configuracion_101.ruta_a_la_plantilla_de_word
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa
    return ruta_completa

def get_ruta_a_carpeta_de_planes_de_crucero(usar_NAS: bool = False):
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = services.doc101.configuracion_101.ruta_a_carpeta_de_planes_de_crucero
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_ruta_al_excel_de_porcentajes():
    """Obtiene un valor de la configuración general de forma dinámica"""
    if not validate_config_value("ruta_al_excel_de_porcentajes", expect_type=str, must_exist_path=True, allow_empty=False):
        return None
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = services.doc101.configuracion_101.ruta_al_excel_de_porcentajes
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa