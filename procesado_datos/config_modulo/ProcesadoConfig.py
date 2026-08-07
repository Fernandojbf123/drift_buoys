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
    
    
    # def get_cantidad_de_decimales(self):
    #     return self.get("cantidad_de_decimales")
    
    # def get_delta_tiempo(self):
    #     return self.get("delta_tiempo")
    
    # def get_nombre_de_la_hoja_con_informacion_de_sondas(self):
    #     return self.get("nombre_de_la_hoja_con_informacion_de_sondas")
    
    # def get_ruta_a_datos_batimetria(self):
    #     return self.get("ruta_a_datos_batimetria")
    
    # def get_ruta_a_datos_topografia(self):
    #     return self.get("ruta_a_datos_topografia")
    
    # def get_formato_de_figuras(self):
    #     return self.get("formato_de_figuras")
    
    # def get_resolucion_de_figuras(self):
    #     return self.get("resolucion_de_figuras")
    
    # def get_origen_de_los_datos(self):
    #     return self.get("origen_de_los_datos")
    
    # def get_decimales_en_figuras(self):
    #     return self.get("decimales_en_figuras")
    
    # def get_tipo_de_letra(self):
    #     return self.get("tipo_de_letra")
    
    # def get_tamanio_de_letra(self):
    #     return self.get("tamanio_de_letra")
    
    # def get_numero_de_bins_histograma(self):
    #     return self.get("numero_de_bins_histograma")
