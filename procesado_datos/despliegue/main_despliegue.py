"""Punto de entrada para procesar las pruebas de despliegue.

Ejecutar desde la raíz del proyecto con:
    python -m procesado_datos.despliegue.main_despliegue_prueba
"""

from pathlib import Path
import sys


# Permite ejecutar este archivo directamente, además de como módulo.
ROOT_PATH = Path(__file__).resolve().parents[2]  #encontrar la raíz del proyecto 
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig
from procesado_datos.config_modulo.config_procesado import config_modulo_procesado
from procesado_datos.despliegue.configs.configuracion_despliegue import config_despliegue
from procesado_datos.despliegue.services.manager_crear_datos_lab import manager_crear_datos_lab


def main() -> None:
    """Crea, guarda y grafica los datos de las pruebas de laboratorio."""
    config = ProcesadoConfig.from_sources(
        config_modulo_procesado,
        config_despliegue,
    )
    manager_crear_datos_lab(config)


if __name__ == "__main__":
    main()
