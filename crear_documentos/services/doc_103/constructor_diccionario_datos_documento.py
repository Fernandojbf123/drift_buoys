import os
import pandas as pd
from configs.manager_doc_config import *

# modulo de construccion de diccionarios para templates de word de ezsnake by BelloDev
from services.word_template_writer import *


# Managers de variables de excel
from services.manager_variables_excel_datos_campania import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_documento import *

# Constructores individuales
from services.doc_103.introduccion_parrafo1 import *
from services.doc_103.bitacora_electronica_parrafo2 import *


############################ DICCIONARIO DE REEMPLAZOS PARA FIGURAS ############################

# ESQUEMA DEL DICCIONARIO DE FIGURAS
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
                
                if varname.lower() == "fig_mapa_de_despliegue".lower():
                    titulo = f"Mapa con los puntos de despliegue de las sondas oceanográficas"
                    dict_temporal.set_titulo(titulo)
                    dict_temporal.set_tamanio(6)  

                if varname.lower() == "fig_esquema_componentes_de_sonda".lower():
                    numero_de_serie = varvalue.split("_")[-1]
                    titulo = f"Figura esquemática con los componentes de las sondas oceanográficas"
                    dict_temporal.set_titulo(titulo)
                    dict_temporal.set_tamanio(6)  
                    
                elif varname.lower() == "fig_mapa_trayectoria".lower():
                    numero_de_serie = varvalue.split("_")[-1]
                    titulo = f"Mapa de trayectoria de la sonda oceanográfica {numero_de_serie} desde su despliegue (punto en color amarillo) hasta el último dato transmitido dentro de la vigencia de la orden de servicio (punto en color rojo)"
                    dict_temporal.set_titulo(titulo)
                    dict_temporal.set_tamanio(6)
                    
                elif varname.lower() == "fig_transmision".lower():
                    
                    fecha_inicio = get_fecha_y_hora_de_embarque_y_campania_unicos(df_datos_documento = df_datos_documento)[0]
                    fecha_final = get_fecha_final_vigencia(df_datos_documento = df_datos_documento)
                    titulo  = f"Series de tiempo de temperatura, las componentes u (Oeste-Este) y v (Sur-Norte), y de la rapidez y dirección"
                    titulo += f"de la corriente superficial de la sonda oceanográfica {numero_de_serie}."
                    titulo += f"La dirección es oceanográfica (hacia dónde va la corriente y medida hacia la derecha a partir del Norte)." 
                    titulo+= f"El periodo va del {fecha_inicio} al {fecha_final}."
                    dict_temporal.set_titulo(titulo)
                    dict_temporal.set_tamanio(6)  
                
                array.append(dict_temporal.return_dict())
                
            dict_documento["<<"+varname+">>"] = array
            
    return dict_documento


############################ DICCIONARIO DE REEMPLAZOS PARA TEXTO ############################
def construir_diccionario_de_datos_documento(df_datos_despliegue: pd.DataFrame, 
                                            df_datos_campanias: pd.DataFrame,
                                            df_datos_documento: pd.DataFrame,
                                            diccionario_de_reemplazos: dict):
    
    ## orden de servicio
    diccionario_de_reemplazos["<<orden_de_servicio>>"] = get_orden_de_servicio()    
    
    ## fechas de vigencia
    diccionario_de_reemplazos["<<fecha_inicio_vigencia>>"] = get_fecha_inicio_vigencia(df_datos_despliegue = df_datos_despliegue)
    diccionario_de_reemplazos["<<fecha_final_vigencia>>"] = get_fecha_final_vigencia(df_datos_despliegue = df_datos_despliegue)
    
    # fecha de entrega
    diccionario_de_reemplazos["<<fecha_de_entrega>>"] = get_fecha_entrega(df_datos_despliegue = df_datos_despliegue)
    
    # seriales de sondas
    diccionario_de_reemplazos["<<seriales_de_sondas>>"] = get_seriales_de_sondas(df_datos_despliegue = df_datos_despliegue)
    diccionario_de_reemplazos["<<numero_de_sondas>>"] = get_numero_de_sondas(df_datos_despliegue = df_datos_despliegue) 
    
    ## mes y_año de liberacion
    diccionario_de_reemplazos["<<mes_y_anio_de_liberacion>>"] = get_mes_y_anio_de_liberacion(df_datos_campanias = df_datos_campanias)
    
    diccionario_de_reemplazos["<<introduccion_parrafo1>>"] = introduccion_parrafo1(df_datos_campanias = df_datos_campanias, 
                                                                                                                        df_datos_despliegue= df_datos_despliegue)
    
    diccionario_de_reemplazos["<<bitacora_electronica_parrafo2>>"] = bitacora_electronica_parrafo2(df_datos_campanias = df_datos_campanias, 
                                                                                                                        df_datos_despliegue= df_datos_despliegue)
    
   
############################# DICCIONARIO DE REEMPLAZOS PARA TABLAS ############################
# Es probable que acá necesite varios esquemas, dependiendo de la tabla.
def construir_diccionario_de_reemplazos_para_tablas(df_datos_despliegue: pd.DataFrame, 
                                                    df_datos_campanias: pd.DataFrame,
                                                    df_datos_documento: pd.DataFrame,
                                                    df_datos_porcentajes: pd.DataFrame,
                                                    diccionario_de_reemplazos: dict,
                                                    doc: object):
    
    
    opciones_de_tabla = OpcionesTabla()
    estilos_de_tabla = EstilosTabla(doc)
    estilos_de_tabla.set_estilo_por_defecto("texto_tablas_centrado")
    
    df_datos_despliegue["serial_de_sonda"] = df_datos_despliegue["serial_de_sonda"].astype(int).astype(str)
    
    equipos = ["GPS primario",
                "GPS secundario", 
                "Sistema de telemetría primario",
                "Sistema de telemetría secundario", 
                "Sensor de temperatura primario",
                "Sensor de temperatura secundario", 
                "Acelerómetro"]    

    seriales = get_seriales_de_sondas(df_datos_despliegue = df_datos_despliegue)
    
    array_secuencia_tabla1 = []
    array_seriales_tabla1 = []
    array_equipos_tabla1 = []
    array_numero_de_serie_de_equipo_tabla1 = []
    
    for secuencia, serial in enumerate(seriales) :
        array_seriales_tabla1.append([serial]*len(equipos))
        array_equipos_tabla1.append(equipos)
        gps_primario = df_datos_despliegue[df_datos_despliegue["serial_de_sonda"] == serial]["gps_primario"].iloc[0]
        gps_secundario = df_datos_despliegue[df_datos_despliegue["serial_de_sonda"] == serial]["gps_secundario"].iloc[0]
        telemetria_primario = df_datos_despliegue[df_datos_despliegue["serial_de_sonda"] == serial]["telemetria_primario"].iloc[0]
        telemetria_secundario = df_datos_despliegue[df_datos_despliegue["serial_de_sonda"] == serial]["telemetria_secundario"].iloc[0]
        temperatura_primario = df_datos_despliegue[df_datos_despliegue["serial_de_sonda"] == serial]["temperatura_primario"].iloc[0]
        temperatura_secundario = df_datos_despliegue[df_datos_despliegue["serial_de_sonda"] == serial]["temperatura_secundario"].iloc[0]
        acelerometro = df_datos_despliegue[df_datos_despliegue["serial_de_sonda"] == serial]["acelerometro"].iloc[0]    
        array_numero_de_serie_de_equipo_tabla1.append([gps_primario, gps_secundario, telemetria_primario, telemetria_secundario, temperatura_primario, temperatura_secundario, acelerometro])
        array_secuencia_tabla1.append([secuencia+1]*len(equipos))
    
    array_secuencia_tabla1 = np.array(array_secuencia_tabla1).flatten()
    array_seriales_tabla1 = np.array(array_seriales_tabla1).flatten()
    array_equipos_tabla1 = np.array(array_equipos_tabla1).flatten()
    array_numero_de_serie_de_equipo_tabla1 = np.array(array_numero_de_serie_de_equipo_tabla1).flatten()
    
    tabla1_dict = {
        "secuencia": array_secuencia_tabla1,
        "serial_de_sonda": array_seriales_tabla1,
        "equipo": array_equipos_tabla1,
        "numero_de_serie_de_equipo": array_numero_de_serie_de_equipo_tabla1
    }
    tabla1 = pd.DataFrame(tabla1_dict)
        
    opciones_de_tabla.set_detectar_merge(True)
    opciones_de_tabla.set_columnas_para_merge([0,1])
    estilos_de_tabla.set_estilo_de_columna(2, "texto_tablas_justificado")
    estilos_de_tabla.set_estilo_de_columna(3, "texto_tablas_justificado")   
    
    diccionario_de_reemplazos["<<tabla_equipos>>"] = {
        "tabla": tabla1,
        "estilos_de_tabla": estilos_de_tabla,
        "opciones_de_tabla": opciones_de_tabla
    }
    
    
    #####################Tabla 3. porcentajes de transmision ##########################
    df_datos_porcentajes["serial_de_sonda"] = df_datos_porcentajes["serial_de_sonda"].astype(int).astype(str)
   
    variables = ["Tempertaura del agua de mar",
                "Posición geográfica", 
                "Rapidez",
                "Dirección"]   
    
    array_seriales_tabla3 = []
    array_fecha_inicio_tabla3 = []
    array_fecha_fin_tabla3 = []
    array_variables_tabla3 = []
    array_cantidad_de_datos_esperados_tabla3 = []
    array_cantidad_de_datos_recibidos_tabla3 = []
    array_porcentaje_de_datos_recibidos_mas_interpolados_tabla3 = []
    
    for serial in enumerate(seriales):
        array_seriales_tabla3.append([serial]*len(variables))
        array_variables_tabla3.append(variables)
        temp = df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["temp"].iloc[0]
        posicion_geografica = df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["posicion_geografica"].iloc[0]
        rapidez = df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["rapidez"].iloc[0]
        direccion = df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["direccion"].iloc[0]
        array_variables_tabla3.append([temp, posicion_geografica, rapidez, direccion])
       
        array_fecha_inicio_tabla3.append([df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["fecha_de_inicio"].iloc[0]]*len(variables))
        array_fecha_fin_tabla3.append([df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["fecha_final"].iloc[0]]*len(variables))
        array_cantidad_de_datos_esperados_tabla3.append([df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["cantidad_de_datos_esperados"].iloc[0]]*len(variables))
        array_cantidad_de_datos_recibidos_tabla3.append([df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["cantidad_de_datos_recibidos"].iloc[0]]*len(variables))
        array_porcentaje_de_datos_recibidos_mas_interpolados_tabla3.append([df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["porcentaje_de_datos_recibidos_mas_interpolados"].iloc[0]]*len(variables))
        array_porcentaje_de_datos_recibidos_mas_interpolados_tabla3.append([df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["porcentaje_de_datos_recibidos_mas_interpolados"].iloc[0]]*len(variables))
    
    
    array_seriales_tabla3 = np.array(array_seriales_tabla3).flatten()
    array_fecha_inicio_tabla3 = np.array(array_fecha_inicio_tabla3).flatten() + "/" + np.array(array_fecha_fin_tabla3).flatten()
    array_variables_tabla3 = np.array(array_variables_tabla3).flatten()
    array_cantidad_de_datos_esperados_tabla3 = np.array(array_cantidad_de_datos_esperados_tabla3).flatten()
    array_cantidad_de_datos_recibidos_tabla3 = np.array(array_cantidad_de_datos_recibidos_tabla3).flatten()
    array_porcentaje_de_datos_recibidos_mas_interpolados_tabla3 = np.array(array_porcentaje_de_datos_recibidos_mas_interpolados_tabla3).flatten()
    array_porcentaje_de_datos_recibidos_mas_interpolados_tabla3 = np.array(array_porcentaje_de_datos_recibidos_mas_interpolados_tabla3).flatten()
    
    tabla3_dict = {
    "serial_de_sonda":  array_seriales_tabla3,
    "fecha_de_inicio": array_fecha_inicio_tabla3,
    "fecha_final": array_fecha_fin_tabla3,
    "cantidad_de_datos_esperados": array_cantidad_de_datos_esperados_tabla3,
    "cantidad_de_datos_recibidos": array_cantidad_de_datos_recibidos_tabla3,
    "porcentaje_de_datos_recibidos_mas_interpolados": array_porcentaje_de_datos_recibidos_mas_interpolados_tabla3,
    "porcentaje_de_datos_recibidos_mas_interpolados": array_porcentaje_de_datos_recibidos_mas_interpolados_tabla3
}
    tabla3 = pd.DataFrame(tabla3_dict)
           
    opciones_de_tabla.set_detectar_merge(True)
    opciones_de_tabla.set_columnas_para_merge([0,1])
    estilos_de_tabla.set_estilo_de_columna(2, "texto_tablas_justificado")
    estilos_de_tabla.set_estilo_de_columna(3, "texto_tablas_justificado")   
    
    diccionario_de_reemplazos["<<tabla_transmision>>"] = {
        "tabla": tabla3,
        "estilos_de_tabla": estilos_de_tabla,
        "opciones_de_tabla": opciones_de_tabla
    }
    
    #################### Tabla 4. Porcentaje de no visualizacion############################     
    
    array_seriales_tabla4 = []
    array_variables_tabla4 = []
    array_cantidad_de_datos_esperados_tabla4 = []
    array_cantidad_de_datos_recibidos_tabla4 = []
    array_porcentaje_de_datos_no_visualizados_tabla4 = []
    
    for serial in enumerate(seriales):
        array_seriales_tabla4.append([serial]*len(variables))
        array_variables_tabla4.append(variables)
        temp = df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["temp"].iloc[0]
        posicion_geografica = df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["posicion_geografica"].iloc[0]
        rapidez = df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["rapidez"].iloc[0]
        direccion = df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["direccion"].iloc[0]
        array_variables_tabla4.append([temp, posicion_geografica, rapidez, direccion])
       
        array_cantidad_de_datos_esperados_tabla4.append([df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["cantidad_de_datos_esperados"].iloc[0]]*len(variables))
        array_cantidad_de_datos_recibidos_tabla4.append([df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["cantidad_de_datos_recibidos"].iloc[0]]*len(variables))
        array_porcentaje_de_datos_no_visualizados_tabla4.append([100 - df_datos_porcentajes[df_datos_porcentajes["serial_de_sonda"] == serial]["porcentaje_de_datos_recibidos_mas_interpolados"].iloc[0]]*len(variables))
       
    
    array_seriales_tabla4 = np.array(array_seriales_tabla4).flatten()
    array_variables_tabla4 = np.array(array_variables_tabla4).flatten()
    array_cantidad_de_datos_esperados_tabla4 = np.array(array_cantidad_de_datos_esperados_tabla4).flatten()
    array_cantidad_de_datos_recibidos_tabla4 = np.array(array_cantidad_de_datos_recibidos_tabla4).flatten()
    array_porcentaje_de_datos_no_visualizados_tabla4 = np.array(array_porcentaje_de_datos_no_visualizados_tabla4).flatten()
  
    tabla4_dict = {
    "serial_de_sonda":  array_seriales_tabla4,
    "cantidad_de_datos_esperados": array_cantidad_de_datos_esperados_tabla4,
    "cantidad_de_datos_recibidos": array_cantidad_de_datos_recibidos_tabla4,
    "porcentaje_de_datos_no_visualizados": array_porcentaje_de_datos_no_visualizados_tabla4
    
}
    tabla4 = pd.DataFrame(tabla4_dict)
           
    opciones_de_tabla.set_detectar_merge(True)
    opciones_de_tabla.set_columnas_para_merge([0,1])
    estilos_de_tabla.set_estilo_de_columna(2, "texto_tablas_justificado")
    estilos_de_tabla.set_estilo_de_columna(3, "texto_tablas_justificado")   
    
    diccionario_de_reemplazos["<<tabla_no_visualizacion>>"] = {
        "tabla": tabla4,
        "estilos_de_tabla": estilos_de_tabla,
        "opciones_de_tabla": opciones_de_tabla
    }