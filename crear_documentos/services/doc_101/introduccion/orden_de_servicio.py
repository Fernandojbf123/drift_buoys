from configs.manager_doc_config import *
from services.manager_variables_excel_datos_despliegue import *

def orden_de_servicio(diccionario_de_reemplazos: dict):
    """ Agrega al diccionario de reemplazos la variable 'orden_de_servicio' con el valor obtenido 
    de la función get_orden_de_servicio()."""
    orden_de_servicio = get_orden_de_servicio()
    diccionario_de_reemplazos["orden_de_servicio"] = orden_de_servicio

