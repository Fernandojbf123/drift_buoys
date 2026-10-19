# Es el manager de las configuraciones comunes para el módulo de procesado de datos.
# Hereda de la clase ConfigManager, que permite cargar configuraciones desde múltiples fuentes y acceder a ellas de manera segura.


import os
from dotenv import load_dotenv
from global_config.ConfigManager import ConfigManager

load_dotenv()

class ProcesadoConfig(ConfigManager):
    
    @property
    def ruta_al_excel_de_despliegue_de_sondas(self):
        ruta = self.get("ruta_al_excel_de_despliegue_de_sondas")
        if not ruta:
            raise ValueError("No se encontró 'ruta_al_excel_de_despliegue_de_sondas' en la configuración.")

        # Si ya es una ruta absoluta local (C:\, D:\, etc.) o una ruta UNC, no se modifica.
        drive, _ = os.path.splitdrive(ruta)
        if drive or ruta.startswith("\\\\"):
            return ruta

        # Si es una ruta relativa, se resuelve contra la ruta base del NAS en .env.
        ruta_al_nas = os.getenv("ruta_al_NAS")
        if not ruta_al_nas:
            raise ValueError(
                "La ruta es relativa y no se encontró la variable de entorno 'ruta_al_NAS'."
            )

        return os.path.join(ruta_al_nas, ruta)
    
    @property
    def ruta_a_carpeta_de_datos_crudos(self):
        ruta = self.get("carpeta_de_datos_crudos")
        if not ruta:
            raise ValueError("No se encontró 'carpeta_de_datos_crudos' en la configuración.")
    
        # Si ya es una ruta absoluta local (C:\, D:\, etc.) o una ruta UNC, no se modifica.
        drive, _ = os.path.splitdrive(ruta)
        if drive or ruta.startswith("\\\\"):
            return ruta

        # Si es una ruta relativa, se resuelve contra la ruta base del NAS en .env.
        ruta_al_nas = os.getenv("ruta_al_NAS")
        if not ruta_al_nas:
            raise ValueError(
                "La ruta es relativa y no se encontró la variable de entorno 'ruta_al_NAS'."
            )
    
        return os.path.join(ruta_al_nas, ruta)