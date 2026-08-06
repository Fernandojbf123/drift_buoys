# Manager de configuración para el proyecto.
# Permite cargar configuraciones desde múltiples fuentes y acceder a ellas de manera segura.
# Todos los módulos y submódulos del proyecto deben utilizar este manager para acceder a sus configuraciones.
# Y los managers
from copy import deepcopy
import pandas as pd

class ConfigManager:
    def __init__(self, data: dict):
        self._data = deepcopy(data)

    # Este método permite crear una instancia de ConfigManager a partir de múltiples diccionarios de configuración 
    # y un diccionario de sobrescritura opcional. Esto me evita errores de clave; además me permite evaluar si una clave existe 
    # en la configuración antes de acceder a ella.
    @classmethod
    def from_sources(cls, *configs: dict, overrides: dict | None = None):
        merged = {}
        for config in configs:
            merged.update(config)
        if overrides:
            merged.update(overrides)
        return cls(merged)
    
    def require(self, *keys: str): # Me permite comprobar que en las configuraciones estén las configuraciones que necesita el módulo
        missing = [key for key in keys if key not in self._data]
        if missing:
            raise KeyError(
                f"Faltan configuraciones obligatorias: {', '.join(missing)}"
            )

    def get(self, key): # para acceder a cualquier clave de configuración, devuelve None si la clave no existe
        return self._data.get(key)
    
    def as_dict(self) -> dict: # devuelve la configuración como un diccionario
        return deepcopy(self._data)

    def __getitem__(self, key: str): # permite acceder a la configuración como si fuera un diccionario, pero lanza un KeyError si la clave no existe
        return self._data[key]

    def __getattr__(self, name: str): # permite acceder a la configuración como si fueran atributos del objeto, pero lanza un AttributeError si la clave no existe
        try:
            return self._data[name]
        except KeyError as exc:
            raise AttributeError(
                f"La configuración '{name}' no existe."
            ) from exc

    def convertir_a_pd_datetime(self, key:str, formato:str="%Y-%m-%d %H:%M:%S"):
        fecha = self.get(key)
        if fecha is None:
            raise ValueError(f"No se encontró la clave '{key}' en la configuración.")
        try:
            fecha_dt = pd.to_datetime(fecha, format=formato)
            return fecha_dt
        except Exception as e:
            raise ValueError(f"Error al convertir la fecha '{fecha}' con el formato '{formato}': {e}")


# def get_fecha_de_inicio_del_analisis(self):
#      fecha = self.get("fecha_de_inicio_del_analisis")
#      fecha = pd.to_datetime(fecha, format="%Y-%m-%d %H:%M:%S")
#      return fecha

# def get_fecha_de_fin_del_analisis(self):
#      fecha = self.get("fecha_de_fin_del_analisis")
#      fecha = pd.to_datetime(fecha, format="%Y-%m-%d %H:%M:%S")
#      return fecha

# def get_delta_tiempo(self):
#     return self.get("delta_tiempo")

# def get_ruta_al_excel_de_despliegue_de_sondas(self):
#     return self.get("ruta_al_excel_de_despliegue_de_sondas")

# def get_nombre_de_la_hoja_con_informacion_de_sondas(self):
#     return self.get("nombre_de_la_hoja_con_informacion_de_sondas")

# def get_carpeta_datos_crudos(self):
#     return self.get("carpeta_de_datos_crudos")

# def get_carpeta_guardado_datos_procesados(self):
#     return self.get("carpeta_de_guardado_de_datos_procesados")

# def get_nombre_archivo_datos_procesados(self):
#     return self.get("nombre_del_archivo_de_datos_procesados")

# def get_nombre_del_archivo_de_datos_previos_a_la_fecha_de_estudio(self):
#     return self.get("nombre_del_archivo_de_datos_previos_a_la_fecha_de_estudio")

# def get_nombre_del_excel_de_porcentajes(self):
#     return self.get("nombre_del_excel_de_porcentajes")

# def get_carpeta_guardado_figuras(self):
#     return self.get("carpeta_de_guardado_de_figuras")

# def get_resolucion_de_figuras(self):
#     return self.get("resolucion_de_figuras")

# def get_seriales_sondas(self):
#     return self.get("seriales_de_sondas")

# def get_formato_figuras(self):
#     return self.get("formato_de_figuras")

# def get_resolucion_figuras(self):
#     return self.get("resolucion_de_figuras")

# def get_origen_de_los_datos(self):
#     return self.get("origen_de_los_datos")

# def get_decimales_figuras(self):
#     return self.get("decimales_en_figuras")

# def get_tipo_letra(self):
#     return self.get("tipo_de_letra")

# def get_tamanio_de_letra(self):
#     return self.get("tamanio_de_letra")

# def get_numero_bins_histograma(self):
#     return self.get("numero_de_bins_histograma")

# def get_variables_graficar(self):
#     return self.get("variables_a_graficar")

# def get_coordenadas_del_mapa(self):
#     return self.get("coordenadas_del_mapa")

# def get_escala_de_color_rapidez(self):
#     return self.get("escala_de_color_rapidez")

# def get_ruta_a_datos_batimetria(self):
#     return self.get("ruta_a_datos_batimetria")

# def get_curvas_de_batimetria(self):
#     curvas = self.get("curvas_de_batimetria")
#     return sorted(curvas)

# def get_graficar_trayectorias_pasadas(self):
#     return self.get("graficar_trayectorias_pasadas")

# def get_ruta_a_datos_topografia(self):
#     return self.get("ruta_a_datos_topografia")
