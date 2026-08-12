import os
import sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

from procesado_datos.despliegue.services.manager_crear_datos_lab import manager_crear_datos_lab
from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig

if __name__ == "__main__":
    # Ejecución standalone del script

    # Importar configuraciones del modulo
    from procesado_datos.config_modulo.config_procesado import config_modulo_procesado
    # Importar configuraciones del submodulo de despliegue
    from procesado_datos.despliegue.configs.configuracion_despliegue import config_despliegue
    
    # Crear la instancia del manager de configuraciones
    config = ProcesadoConfig.from_sources(
        config_modulo_procesado,
        config_despliegue,
    )    
    
    ## LLamar al manager; se encarga de llamar la creación de datos, guardar, y graficar
    manager_crear_datos_lab(config)

else:
    # Ejecución como módulo
    print("Se llama como modulo")
    
    # manager_crear_datos_lab(config)