import os
import pandas as pd
from configs.manager_doc_config import *
from services.manager_variables_excel_documento import *

####################### ESQUEMA DE DICCIONARIO PARA FIGURAS #######################
class Dictfiguras():
    def __init__(self):
        self.ruta = ""
        self.titulo = ""
        self.tamanio = 6
        self.bookmark = ""

    def set_ruta(self, varvalue: str):
        carpeta = get_ruta_a_carpeta_de_las_figuras(usar_NAS=True)
        ruta_completa = os.path.join(carpeta, varvalue+".jpg")
        self.ruta = ruta_completa.strip()
    
    def set_tamanio(self, tamanio: int):
        self.tamanio = tamanio
    
    def set_bookmark(self, varvalue: str):
        bookmark = "Ref_"+varvalue
        self.bookmark = bookmark.strip()
        
    def set_titulo(self, varvalue: str):
        titulo = varvalue.strip() 
        titulo = titulo if titulo.endswith(".") else titulo + "."
        self.titulo = titulo
        
    def return_dict(self) -> dict:
        return {
            "ruta": self.ruta,
            "titulo": self.titulo,
            "tamanio": self.tamanio,
            "bookmark": self.bookmark
        }
  
#######################################


def construir_diccionario_agregar_figuras(df_datos_documento: pd.DataFrame) -> dict:
    dict_documento = {}
    varnames_documento = get_varnames_documento(df_datos_documento = df_datos_documento) 

    for ivarname, varname in enumerate(varnames_documento):
        varvalues = get_variable_documento(df_datos_documento = df_datos_documento, nombre_variable = varname)
        if varname.startswith("fig_"):
            dict_temporal = Dictfiguras()  
            array=[]
            for ivarvalue, varvalue in enumerate(varvalues):
                dict_temporal.set_ruta(varvalue)
                dict_temporal.set_tamanio(3) 
                dict_temporal.set_bookmark(varvalue)
                dict_temporal.set_titulo("")
                next_varname = varnames_documento[ivarname+1]
                
                if next_varname.startswith("pie_"):
                    pie_value = get_variable_documento(df_datos_documento = df_datos_documento, nombre_variable = next_varname)
                    dict_temporal.set_titulo(pie_value[ivarvalue])
                
                elif varname.lower() == "fig_esquemas_sondas".lower():
                    numero_de_serie = varvalue.split("_")[-1]
                    titulo = f"Despliegue de sonda oceanográfica {numero_de_serie}"
                    dict_temporal.set_titulo(titulo)
                    
                elif varname.lower() == "fig_pruebas_transmision".lower():
                    numero_de_serie = varvalue.split("_")[-1]
                    titulo = f"Datos enviados durante las pruebas de laboratorio para la sonda {numero_de_serie}"
                    dict_temporal.set_titulo(titulo)
                    
                elif varname.lower() == "fig_pruebas_baterias".lower():
                    titulo = f"Datos transmitidos del estado de las baterias durante las 24 horas de las pruebas de funcionamiento"
                    dict_temporal.set_titulo(titulo)    
                
                elif varname.lower() == "fig_ubicacion_durante_pruebas".lower():
                    titulo = f"Mapa con la información con las primeras 24 horas de transmisión de las sondas"
                    dict_temporal.set_titulo(titulo)

                array.append(dict_temporal.return_dict())
                
            dict_documento["<<"+varname+">>"] = array
            
    return dict_documento

            
            

# # dict_demo = {
# #     get_variable_documento(df_datos_documento = df_documento, nombre_variable = "anio_de_vigencia"),
# #     "<<mes_de_vigencia>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "mes_de_vigencia"),
# #     "<<fig_descripcion_arquitectura>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_descripcion_arquitectura"),
# #     "<<pie_descripcion_arquitectura>>": get_variable_documento(df_datos_documento   = df_documento, nombre_variable = "pie_descripcion_arquitectura"),
# #     "<<fig_actividades_previas>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_actividades_previas"),
# #     "<<pie_actividades_previas>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "pie_actividades_previas"),
# #     "<<anio_de_vigencia>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "anio_de_vigencia"),
# #     "<<mes_de_vigencia>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "mes_de_vigencia"),
# #     "<<fig_descripcion_arquitectura>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_descripcion_arquitectura"),
# #     "<<pie_descripcion_arquitectura>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "pie_descripcion_arquitectura"),
# #     "<<fig_actividades_previas>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_actividades_previas"),
# #     "<<pie_actividades_previas>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "pie_actividades_previas"),
# #     "<<fig_mapa_de_despliegue>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_mapa_de_despliegue"),
# #     "<<pie_mapa_de_despliegue>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "pie_mapa_de_despliegue"),
# #     "<<fig_ejecucion_campania>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_ejecucion_campania"),
# #     "<<pie_ejecucion_campania>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "pie_ejecucion_campania"),
# #     "<<fig_esquemas_sondas>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_esquemas_sondas"),
# #     "<<fig_pruebas_baterias>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_pruebas_baterias"),
# #     "<<fig_ubicacion_durante_pruebas>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_ubicacion_durante_pruebas"),
# #     "<<fig_pruebas_de_funcionamiento>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_pruebas_de_funcionamiento"),
# #     "<<fig_pruebas_transmision>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_pruebas_transmision"),
# #     "<<ruta_plan_de_crucero>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "ruta_plan_de_crucero"),
# #     "<<fig_anexo_fotografico>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "fig_anexo_fotografico"),
# #     "<<descripcion_anexo_fotografico>>": get_variable_documento(df_datos_documento = df_documento, nombre_variable = "descripcion_anexo_fotografico")
# # }