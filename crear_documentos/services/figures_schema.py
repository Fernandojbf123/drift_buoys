import os

# Esquema (contrato) compartido que define las reglas para construir la
# variable de una figura. No construye el diccionario de reemplazos: los
# constructores (constructor_diccionario_datos_documento.py de doc_101 y
# doc_103) son quienes usan este esquema para armar el diccionario final.

# ESQUEMA DEL DICCIONARIO DE FIGURAS
class Dictfiguras():
    def __init__(self, ruta_a_carpeta_de_figuras):
        self.ruta_a_carpeta_de_figuras = ruta_a_carpeta_de_figuras
        self.ruta = ""
        self.titulo = ""
        self.tamanio = 6
        self.bookmark = ""

    def set_ruta(self, varvalue: str):
        extensiones = [".png", ".jpg", ".jpeg", ".tiff", ".tif"]
        ruta_completa = None

        for ext in extensiones:
            posible_ruta = os.path.join(self.ruta_a_carpeta_de_figuras, varvalue + ext)
            if os.path.exists(posible_ruta):
                ruta_completa = posible_ruta
                break
        if ruta_completa is None:
            raise FileNotFoundError(f"No se encontró la imagen: {varvalue} con extensiones {extensiones}")
        self.ruta = ruta_completa  

    def set_tamanio(self, tamanio: int):
        self.tamanio = tamanio

    def set_bookmark(self, varvalue: str):
        bookmark = "Ref_"+varvalue
        self.bookmark = bookmark.strip()

    def set_titulo(self, varvalue: str):
        titulo = varvalue.strip() 
        if titulo != "":
            titulo = titulo if titulo.endswith(".") else titulo + "."
        self.titulo = titulo

    def return_dict(self) -> dict:
        return {
            "ruta": self.ruta,
            "titulo": self.titulo,
            "tamanio": self.tamanio,
            "bookmark": self.bookmark
        }
