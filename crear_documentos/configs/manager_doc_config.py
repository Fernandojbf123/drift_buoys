import os
import dotenv

dotenv.load_dotenv()  # Carga las variables de entorno desde el archivo .env
class configuracion_documentos():
    def __init__(self, config):
        self.config = config

    def __getattr__(self, propiedad):
        return self.get(propiedad)

    def get(self, propiedad):
        return self.config.get(propiedad)

    def __getitem__(self, propiedad):
        return getattr(self, propiedad)

    def get_orden_de_servicio(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        return self.get("orden_de_servicio")

    def get_fecha_de_solicitud(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        return self.get("fecha_de_solicitud")

    def get_ruta_al_excel_para_crear_documento(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_al_excel_para_crear_documento")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa

    def get_hoja_del_excel_para_crear_documento(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        return self.get("hoja_del_excel_para_crear_documento")

    def get_ruta_a_carpeta_de_las_figuras(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_a_carpeta_de_las_figuras")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa

    def get_ruta_a_carpeta_de_guardado_del_documento(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_a_carpeta_de_guardado_del_documento")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa

    def get_ruta_al_excel_de_despliegue_de_sondas(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_al_excel_de_despliegue_de_sondas")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa

    def get_hoja_del_excel_de_despliegue_de_sondas(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        return self.get("hoja_del_excel_de_despliegue_de_sondas")

    def get_ruta_al_excel_de_campanias(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("rutal_al_excel_de_campanias")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa

    def get_hoja_del_excel_de_campanias(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        return self.get("hoja_del_excel_de_campanias")

    def get_usar_NAS(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        return self.get("usar_NAS")

    def get_ruta_a_la_plantilla_de_word(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_a_la_plantilla_de_word")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa

    def get_ruta_a_la_plantilla_de_ppt(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_a_la_plantilla_de_ppt")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa

    def get_ruta_a_la_plantilla_de_pruebas(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_a_la_plantilla_de_pruebas")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa

    def get_ruta_a_carpeta_de_planes_de_crucero(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_a_carpeta_de_planes_de_crucero")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa

    def get_ruta_al_excel_de_porcentajes(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_a_la_carpeta_de_despliegue")
        archivo = self.get("nombre_del_excel_de_porcentajes")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta, archivo)   
        else:
            ruta_completa = os.path.join(carpeta, archivo)  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa
    
    def get_ruta_a_la_carpeta_de_despliegue(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_a_la_carpeta_de_despliegue")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa
    
    def get_ruta_a_carpeta_de_plantilla(self):
        """Obtiene un valor de la configuración general de forma dinámica"""
        ruta_al_NAS = os.getenv("ruta_al_NAS")
        carpeta = self.get("ruta_a_carpeta_de_plantilla")
        if self.get_usar_NAS() and ruta_al_NAS:
            ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
        else:
            ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
        return ruta_completa