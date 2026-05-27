import os
import pandas as pd
from configs.manager_doc_config import *

# modulo de construccion de diccionarios para templates de word de ezsnake by BelloDev
from services.word_template_writer import *


# Managers de variables de excel
from services.manager_variables_excel_datos_campania import *
from services.manager_variables_excel_datos_despliegue import *
from services.manager_variables_excel_documento import *
from services.doc_103.manager_porcentajes import *

# Constructores individuales
from services.doc_103.introduccion_parrafo1 import *
from services.doc_103.bitacora_electronica_parrafo1 import *


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

        extensiones = [".png", ".jpg", ".jpeg", ".tiff", ".tif"]

        ruta_completa = None

        for ext in extensiones:
            posible_ruta = os.path.join(carpeta, varvalue + ext)

            if os.path.exists(posible_ruta):
                ruta_completa = posible_ruta
                break

        # VALIDACIÓN DE EXISTENCIA DE LA IMAGEN
        if ruta_completa is None:
            raise FileNotFoundError(
                f"No se encontró la imagen: {varvalue} con extensiones {extensiones}"
            )

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

def construir_diccionario_agregar_figuras(
    df_datos_documento: pd.DataFrame,
    df_datos_despliegue: pd.DataFrame,
    df_datos_campanias: pd.DataFrame
) -> dict:

    dict_documento = {}
    varnames_documento = get_varnames_documento(df_datos_documento=df_datos_documento)

    for ivarname, varname in enumerate(varnames_documento):

        varvalues = get_variable_documento(
            df_datos_documento=df_datos_documento,
            nombre_variable=varname
        )

        # SOLO FIGURAS
        if varname.startswith("fig_"):

            lista_figuras = [] 

            next_varname = (
                varnames_documento[ivarname + 1]
                if ivarname + 1 < len(varnames_documento)
                else None
            )

            for ivarvalue, varvalue in enumerate(varvalues):

                dict_temporal = Dictfiguras()

                dict_temporal.set_ruta(varvalue)
                dict_temporal.set_tamanio(3)
                dict_temporal.set_bookmark(varvalue)
                dict_temporal.set_titulo("")

                # PIE
                if isinstance(next_varname, str) and next_varname.startswith("pie_"):

                    pie_value = get_variable_documento(
                        df_datos_documento=df_datos_documento,
                        nombre_variable=next_varname
                    )

                    if ivarvalue < len(pie_value):
                        dict_temporal.set_titulo(pie_value[ivarvalue])

                # CASOS ESPECIALES
                if varname.lower() == "fig_mapa_de_despliegue".lower():
                    dict_temporal.set_titulo("Mapa con los puntos de despliegue de las sondas oceanográficas")
                    dict_temporal.set_tamanio(6)

                elif varname.lower() == "fig_esquema_componentes_de_sonda".lower():
                    dict_temporal.set_titulo("Figura esquemática con los componentes de las sondas oceanográficas")
                    dict_temporal.set_tamanio(6)

                elif varname.lower() == "fig_mapa_trayectoria".lower():
                    numero_de_serie = varvalue.split("_")[-1]
                    titulo = (
                        f"Mapa de trayectoria de la sonda oceanográfica {numero_de_serie} "
                        f"desde su despliegue hasta el último dato."
                    )
                    dict_temporal.set_titulo(titulo)
                    dict_temporal.set_tamanio(6)

                elif varname.lower() == "fig_transmision".lower():
                    fecha_inicio = get_dia_de_liberacion(df_datos_campanias=df_datos_campanias) 
                    fecha_final = get_fecha_final_vigencia(df_datos_despliegue=df_datos_despliegue)

                    titulo = (
                        "Series de tiempo de temperatura, componentes u y v, rapidez y dirección "
                        f"de la sonda oceanográfica. "
                        f"El periodo va del {fecha_inicio} al {fecha_final}."
                    )

                    dict_temporal.set_titulo(titulo)
                    dict_temporal.set_tamanio(6)
                    

                lista_figuras.append(dict_temporal.return_dict())

            # guardar en diccionario final
            dict_documento["<<"+varname+">>"] = lista_figuras

    return dict_documento

############################ DICCIONARIO DE REEMPLAZOS PARA TEXTO ############################
def construir_diccionario_de_datos_documento(df_datos_despliegue: pd.DataFrame, 
                                            df_datos_campanias: pd.DataFrame,
                                            df_datos_documento: pd.DataFrame,
                                            df_porcentajes: pd.DataFrame,
                                            diccionario_de_reemplazos: dict):
    
    ## orden de servicio
    diccionario_de_reemplazos["<<orden_de_servicio>>"] = get_orden_de_servicio()    
    # fecha de solicitud
    diccionario_de_reemplazos["<<fecha_de_solicitud>>"] = get_fecha_de_solicitud()    
    
    ## fechas de vigencia
    diccionario_de_reemplazos["<<fecha_inicio_vigencia>>"] = get_fecha_inicio_vigencia(df_datos_despliegue = df_datos_despliegue)
    diccionario_de_reemplazos["<<fecha_final_vigencia>>"] = get_fecha_final_vigencia(df_datos_despliegue = df_datos_despliegue)
    
    # fecha de entrega
    diccionario_de_reemplazos["<<fecha_de_entrega>>"] = get_fecha_entrega(df_datos_despliegue = df_datos_despliegue)
    
    # seriales de sondas
    seriales_de_sondas = get_seriales_de_sondas(df_datos_despliegue = df_datos_despliegue)
    diccionario_de_reemplazos["<<seriales_de_sondas>>"] = ", ".join([str(serial) for serial in seriales_de_sondas])  # Convierte a string con formato "12345, 67890"
   
    diccionario_de_reemplazos["<<numero_de_sondas>>"] = get_numero_de_sondas(df_datos_despliegue = df_datos_despliegue) 
    
    ## mes y_año de liberacion
    diccionario_de_reemplazos["<<mes_y_anio_de_liberacion>>"] = get_mes_y_anio_de_liberacion(df_datos_campanias = df_datos_campanias)
    
    diccionario_de_reemplazos["<<introduccion_parrafo1>>"] = introduccion_parrafo1(df_datos_campanias = df_datos_campanias, 
                                                                                                                        df_datos_despliegue= df_datos_despliegue)
    
    diccionario_de_reemplazos["<<bitacora_electronica_parrafo1>>"] = bitacora_electronica_parrafo1(df_datos_campanias = df_datos_campanias, 
                                                                                                                        df_datos_despliegue= df_datos_despliegue)
    diccionario_de_reemplazos["<<fecha_inicio>>"] = get_dia_de_liberacion(df_datos_campanias = df_datos_campanias)
    
    diccionario_de_reemplazos["<<porcentaje_de_transmision>>"] = get_porcentaje_maximo_de_transmision(df_porcentajes = df_porcentajes)
    
    diccionario_de_reemplazos["<<periodo_de_transmision>>"] = get_periodo_de_transmision(df_porcentajes = df_porcentajes)
   
############################# DICCIONARIO DE REEMPLAZOS PARA TABLAS ############################
# Es probable que acá necesite varios esquemas, dependiendo de la tabla.
def construir_diccionario_de_reemplazos_para_tablas(df_datos_despliegue: pd.DataFrame, 
                                                    df_datos_campanias: pd.DataFrame,
                                                    df_datos_documento: pd.DataFrame,
                                                    df_porcentajes: pd.DataFrame,
                                                    diccionario_de_reemplazos: dict,
                                                    doc: object):
    
    opciones_de_tabla = OpcionesTabla()
    estilos_de_tabla = EstilosTabla(doc)
    estilos_de_tabla.set_estilo_por_defecto("texto_tablas_centrado")
    
    tabla1 = df_datos_despliegue[["serial_de_sonda","latitud_plan","longitud_plan","fecha_y_hora_de_despliegue_maniobra","estado_despliegue"]]
    tabla1.insert(0,"secuencia", range(1, len(tabla1) + 1))
    tabla1["secuencia"] = tabla1["secuencia"].astype(int).astype(str)
    tabla1["serial_de_sonda"] = tabla1["serial_de_sonda"].astype(int).astype(str)
    tabla1["latitud_plan"] = tabla1["latitud_plan"].astype(str)
    tabla1["longitud_plan"] = tabla1["longitud_plan"].astype(str)
    tabla1["fecha_y_hora_de_despliegue_maniobra"] = pd.to_datetime(tabla1["fecha_y_hora_de_despliegue_maniobra"], format = "%d/%m/%Y %H:%M:%S").dt.strftime("%d/%m/%Y %H:%M")
    diccionario_de_reemplazos["<<tabla_equipos>>"] = {
        "tabla": tabla1,
        "estilos_de_tabla": estilos_de_tabla,
        "opciones_de_tabla": opciones_de_tabla
    }

    
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
    df_porcentajes["serial_de_sonda"] = df_porcentajes["serial_de_sonda"].astype(str)

    variables = [
        "Temperatura del agua de mar",
        "Posición geográfica",
        "Rapidez",
        "Dirección"
    ]

    # 1. Expandir filas (serial × variables)
    df_expanded = (
        df_porcentajes
        .loc[df_porcentajes.index.repeat(len(variables))]
        .copy()
        .reset_index(drop=True)
    )

    # 2. Asignar variables
    df_expanded["variable"] = variables * len(df_porcentajes)

    # 3. Fecha inicio / fin van en una columna
    df_expanded["fecha_inicio_fin"] = (
        df_expanded["fecha_de_inicio"].astype(str)
        + " / " +
        df_expanded["fecha_final"].astype(str)
    )

    # 4. Métricas repetidas automáticamente
    df_expanded["cantidad_de_datos_esperados"] = df_expanded["cantidad_de_datos_esperados"]
    df_expanded["cantidad_de_datos_recibidos"] = df_expanded["cantidad_de_datos_recibidos"]

    # 5. Porcentajes repetidos en ambas columnas (como pediste)
    df_expanded["porcentaje"] = df_expanded["porcentaje_de_datos_recibidos_mas_interpolados"]

    df_expanded["porcentaje_de_transmision"] = df_expanded["porcentaje"]
    df_expanded["porcentaje_de_visualizacion"] = df_expanded["porcentaje"]

    # 6. Tabla final lista para Word
    tabla3 = df_expanded[[
        "serial_de_sonda",
        "fecha_inicio_fin",
        "variable",
        "cantidad_de_datos_esperados",
        "cantidad_de_datos_recibidos",
        "porcentaje_de_transmision",
        "porcentaje_de_visualizacion"
    ]]
           
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
    # 1. Expandir filas (serial × variables)
    df_expanded = (
        df_porcentajes
        .loc[df_porcentajes.index.repeat(len(variables))]
        .copy()
        .reset_index(drop=True)
    )

    # 2. Asignar variables
    df_expanded["variable"] = variables * len(df_porcentajes)

    # 3. Métricas base
    df_expanded["cantidad_de_datos_esperados"] = df_expanded["cantidad_de_datos_esperados"]
    df_expanded["cantidad_de_datos_recibidos"] = df_expanded["cantidad_de_datos_recibidos"]

    # 4. Porcentaje visualizado (base)
    df_expanded["porcentaje_visualizado"] = df_expanded["porcentaje_de_datos_recibidos_mas_interpolados"]

    # 5. Porcentaje NO visualizado
    df_expanded["porcentaje_no_visualizado"] = 100 - df_expanded["porcentaje_visualizado"].round(2)

    # 6. Tabla final
    tabla4 = df_expanded[[
        "serial_de_sonda",
        "variable",
        "cantidad_de_datos_esperados",
        "cantidad_de_datos_recibidos",
        "porcentaje_no_visualizado"
    ]]
    
    opciones_de_tabla.set_detectar_merge(True)
    opciones_de_tabla.set_columnas_para_merge([0,1])
    estilos_de_tabla.set_estilo_de_columna(2, "texto_tablas_justificado")
    estilos_de_tabla.set_estilo_de_columna(3, "texto_tablas_justificado")   
    
    
    diccionario_de_reemplazos["<<tabla_no_visualizacion>>"] = {
        "tabla": tabla4,
        "estilos_de_tabla": estilos_de_tabla,
        "opciones_de_tabla": opciones_de_tabla
    }
    