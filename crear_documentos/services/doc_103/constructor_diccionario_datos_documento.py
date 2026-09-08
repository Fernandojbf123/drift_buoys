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
            "bookmark": self.bookmark}

def construir_diccionario_agregar_figuras(df_datos_documento: pd.DataFrame, df_datos_despliegue: pd.DataFrame, df_datos_campanias: pd.DataFrame, df_porcentajes: pd.DataFrame) -> dict:
    dict_documento = {}
    varnames_documento = get_varnames_documento(df_datos_documento=df_datos_documento)

    for ivarname, varname in enumerate(varnames_documento):
        varvalues = get_variable_documento(
            df_datos_documento=df_datos_documento,
            nombre_variable=varname)

        if varname.startswith("fig_"):

            lista_figuras = [] 
            next_varname = (varnames_documento[ivarname + 1]
                if ivarname + 1 < len(varnames_documento)
                else None)

            for ivarvalue, varvalue in enumerate(varvalues):

                dict_temporal = Dictfiguras()
                dict_temporal.set_ruta(varvalue)
                dict_temporal.set_tamanio(3)
                dict_temporal.set_bookmark(varvalue)
                dict_temporal.set_titulo("")

                # PIE
                if isinstance(next_varname, str) and next_varname.startswith("pie_"):

                    pie_value = get_variable_documento(df_datos_documento=df_datos_documento, nombre_variable=next_varname)

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
                    numero_de_serie = varvalue.split("_")[-1]
                    periodo = get_periodo_transmision_sonda_individual(df_porcentajes=df_porcentajes, serial_de_sonda= str(numero_de_serie))

                    titulo = ("Series de tiempo de temperatura, componentes u y v, rapidez y dirección "
                        f"de la sonda oceanográfica {numero_de_serie}. "
                        f"El periodo va {periodo}.")

                    dict_temporal.set_titulo(titulo)
                    dict_temporal.set_tamanio(6)
                    

                lista_figuras.append(dict_temporal.return_dict())

            # guardar en diccionario final
            dict_documento["<<"+varname+">>"] = lista_figuras

    return dict_documento
    
############################ DICCIONARIO DE REEMPLAZOS PARA TEXTO ############################

def construir_diccionario_de_portada(df_datos_despliegue: pd.DataFrame, 
                                    df_datos_campanias: pd.DataFrame,
                                    df_datos_documento: pd.DataFrame,
                                    diccionario_de_reemplazos: dict):
    # seriales de sondas
    seriales_de_sondas = get_seriales_de_sondas(df_datos_despliegue = df_datos_despliegue)
    diccionario_de_reemplazos["<<seriales_de_sondas>>"] = ", ".join([str(serial) for serial in seriales_de_sondas])  
    diccionario_de_reemplazos["<<fecha_inicio_vigencia_portada>>"] = (get_fecha_inicio_vigencia_portada(df_datos_despliegue = df_datos_despliegue))
    diccionario_de_reemplazos["<<mes_anio_portada>>"] = get_mes_anio_portada(df_datos_despliegue = df_datos_despliegue)
    diccionario_de_reemplazos["<<orden_de_servicio>>"] = get_orden_de_servicio_103()   
    diccionario_de_reemplazos["<<fecha_final_vigencia>>"] = get_fecha_final_vigencia(df_datos_despliegue = df_datos_despliegue)
    
def construir_diccionario_de_datos_documento(df_datos_despliegue: pd.DataFrame, 
                                            df_datos_campanias: pd.DataFrame,
                                            df_porcentajes: pd.DataFrame,
                                            df_datos_documento: pd.DataFrame,
                                            diccionario_de_reemplazos: dict):
   
    ## orden de servicio
    diccionario_de_reemplazos["<<orden_de_servicio>>"] = get_orden_de_servicio_103()    
    # fecha de solicitud
    diccionario_de_reemplazos["<<fecha_de_solicitud>>"] = get_fecha_de_solicitud()    
    
    ## fechas de vigencia
    diccionario_de_reemplazos["<<fecha_inicio_vigencia>>"] = get_fecha_inicio_vigencia_texto(df_datos_despliegue = df_datos_despliegue)
    diccionario_de_reemplazos["<<dia_inicio_vigencia>>"] = get_dia_inicio_vigencia(df_datos_despliegue = df_datos_despliegue)
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
    diccionario_de_reemplazos["<<bitacora_electronica_parrafo1>>"] = bitacora_electronica_parrafo1(df_datos_despliegue = df_datos_despliegue, df_porcentajes = df_porcentajes)
    diccionario_de_reemplazos["<<fecha_inicio>>"] = get_dia_de_liberacion(df_porcentajes= df_porcentajes)
    
    diccionario_de_reemplazos["<<porcentaje_de_transmision>>"] = get_porcentaje_maximo_de_transmision(df_porcentajes = df_porcentajes)
    
    diccionario_de_reemplazos["<<periodo_de_transmision>>"] = get_periodo_de_transmision(df_porcentajes = df_porcentajes)
    
############################# DICCIONARIO DE REEMPLAZOS PARA TABLAS ############################
def construir_diccionario_de_reemplazos_para_tablas(
    df_datos_despliegue: pd.DataFrame,
    df_porcentajes: pd.DataFrame,
    df_datos_campanias: pd.DataFrame,
    diccionario_de_reemplazos: dict,
    doc: object
):
    """
    Construye los datos y configuraciones para las tablas 1, 2 y 3
    del documento.

    Tabla 1:
        <<tabla_equipos>>
        <<titulo_tabla_1>>
        <<ref_tabla_1>>

    Tabla 2:
        <<tabla_transmision>>
        <<titulo_tabla_2>>
        <<ref_tabla_2>>

    Tabla 3:
        <<tabla_no_visualizacion>>
        <<titulo_tabla_3>>
        <<ref_tabla_3>>
    """
    # =========================================================
    # MES Y AÑO DE LIBERACIÓN
    # =========================================================

    mes_y_anio_de_liberacion = get_mes_y_anio_de_liberacion(
        df_datos_campanias=df_datos_campanias)
    # =========================================================
    # PREPARACIÓN GENERAL DE DATOS
    # =========================================================

    df_datos_despliegue = df_datos_despliegue.copy()

    df_datos_despliegue["serial_de_sonda"] = (
        df_datos_despliegue["serial_de_sonda"].astype(str))
    
    equipos = [
        "GPS primario",
        "GPS secundario",
        "Sistema de telemetría primario",
        "Sistema de telemetría secundario",
        "Sensor de temperatura primario",
        "Sensor de temperatura secundario",
        "Acelerómetro"]

    seriales = get_seriales_de_sondas(
        df_datos_despliegue=df_datos_despliegue)

    # =========================================================
    # TABLA 1 - EQUIPOS
    # =========================================================

    array_secuencia_tabla_equipos = []
    array_seriales_tabla_equipos = []
    array_equipos_tabla_equipos = []
    array_numero_de_serie_de_equipo_tabla_equipos = []

    for secuencia, serial in enumerate(seriales):

        datos_sonda = df_datos_despliegue[
            df_datos_despliegue["serial_de_sonda"] == serial].iloc[0]

        # Serial de la sonda repetido para cada equipo
        array_seriales_tabla_equipos.append(
            [serial] * len(equipos))

        # Nombre de cada equipo
        array_equipos_tabla_equipos.append(equipos)

        # Número de serie de cada equipo
        array_numero_de_serie_de_equipo_tabla_equipos.append([
            datos_sonda["gps_primario"],
            datos_sonda["gps_secundario"],
            datos_sonda["telemetria_primario"],
            datos_sonda["telemetria_secundario"],
            datos_sonda["temperatura_primario"],
            datos_sonda["temperatura_secundario"],
            datos_sonda["acelerometro"]])

        # Número de secuencia
        array_secuencia_tabla_equipos.append(
            [secuencia + 1] * len(equipos))

    # ---------------------------------------------------------
    # Aplanar arrays
    # ---------------------------------------------------------

    array_secuencia_tabla_equipos = (
        np.array(
            array_secuencia_tabla_equipos
        ).flatten())

    array_seriales_tabla_equipos = (
        np.array(
            array_seriales_tabla_equipos
        ).flatten())

    array_equipos_tabla_equipos = (
        np.array(
            array_equipos_tabla_equipos
        ).flatten())

    array_numero_de_serie_de_equipo_tabla_equipos = (
        np.array(
            array_numero_de_serie_de_equipo_tabla_equipos
        ).flatten())

    # ---------------------------------------------------------
    # DataFrame de tabla 1
    # ---------------------------------------------------------

    tabla_equipos_dict = {
        "secuencia": array_secuencia_tabla_equipos,
        "serial_de_sonda": array_seriales_tabla_equipos,
        "equipo": array_equipos_tabla_equipos,
        "numero_de_serie_de_equipo":
            array_numero_de_serie_de_equipo_tabla_equipos}

    tabla_equipos = pd.DataFrame(
        tabla_equipos_dict)

    # ---------------------------------------------------------
    # Configuración tabla 1
    # ---------------------------------------------------------

    opciones_tabla_1 = OpcionesTabla()
    estilos_tabla_1 = EstilosTabla(doc)

    estilos_tabla_1.set_estilo_por_defecto(
        "texto_tablas_centrado")

    opciones_tabla_1.set_detectar_merge(True)

    opciones_tabla_1.set_columnas_para_merge(
        [0, 1])

    estilos_tabla_1.set_estilo_de_columna(
        2,
        "texto_tablas_centrado")

    estilos_tabla_1.set_estilo_de_columna(
        3,
        "texto_tablas_centrado")

    # ---------------------------------------------------------
    # Registrar tabla 1
    # ---------------------------------------------------------

    diccionario_de_reemplazos["<<tabla_equipos>>"] = {
        "tabla": tabla_equipos,
        "estilos_de_tabla": estilos_tabla_1,
        "opciones_de_tabla": opciones_tabla_1
    }

    # ---------------------------------------------------------
    # Título tabla 1
    # ---------------------------------------------------------

    diccionario_de_reemplazos["<<titulo_tabla_1>>"] = {
        "texto": (
            "Relación de los números de serie de equipos y "
            "sensores instalados en las sondas oceanográficas "
            f"durante {mes_y_anio_de_liberacion}.")
    }

    # ---------------------------------------------------------
    # Referencia tabla 1
    # ---------------------------------------------------------

    diccionario_de_reemplazos["<<ref_tabla_1>>"] = [
        "tabla_1"]

    # =========================================================
    # TABLA 2 - PORCENTAJE DE TRANSMISIÓN
    # =========================================================

    df_porcentajes = df_porcentajes.copy()

    df_porcentajes["serial_de_sonda"] = (
        df_porcentajes["serial_de_sonda"].astype(str))

    variables = [
        "Temperatura del agua de mar",
        "Posición geográfica",
        "Rapidez",
        "Dirección"]

    # ---------------------------------------------------------
    # Expandir: una fila por variable
    # ---------------------------------------------------------

    df_expanded = (
        df_porcentajes
        .loc[df_porcentajes.index.repeat(len(variables))].copy().reset_index(drop=True))

    df_expanded["variable"] = (
        variables * len(df_porcentajes))

    df_expanded["fecha_inicio_fin"] = (
        df_expanded["fecha_de_inicio"].astype(str)
        + " / "
        + df_expanded["fecha_final"].astype(str))

    df_expanded["porcentaje"] = (
        df_expanded["porcentaje_de_datos_recibidos"])

    df_expanded["porcentaje_de_transmision"] = (
        df_expanded["porcentaje"])

    df_expanded["porcentaje_de_visualizacion"] = (
        df_expanded["porcentaje"])

    # ---------------------------------------------------------
    # DataFrame tabla 2
    # ---------------------------------------------------------

    tabla3 = df_expanded[
        [
            "serial_de_sonda",
            "fecha_inicio_fin",
            "variable",
            "cantidad_de_datos_esperados",
            "cantidad_de_datos_recibidos",
            "porcentaje_de_transmision",
            "porcentaje_de_visualizacion"
        ]].copy()

    # ---------------------------------------------------------
    # Configuración tabla 2
    # ---------------------------------------------------------

    opciones_tabla_2 = OpcionesTabla()
    estilos_tabla_2 = EstilosTabla(doc)

    estilos_tabla_2.set_estilo_por_defecto(
        "texto_tablas_centrado")

    opciones_tabla_2.set_detectar_merge(True)

    opciones_tabla_2.set_columnas_para_merge(
        [0, 1])

    estilos_tabla_2.set_estilo_de_columna(
        2,
        "texto_tablas_centrado")

    estilos_tabla_2.set_estilo_de_columna(
        3,
        "texto_tablas_centrado")

    estilos_tabla_2.set_estilo_de_columna(
        4,
        "texto_tablas_centrado")

    estilos_tabla_2.set_estilo_de_columna(
        5,
        "texto_tablas_centrado")

    estilos_tabla_2.set_estilo_de_columna(
        6,
        "texto_tablas_centrado")

    # ---------------------------------------------------------
    # Registrar tabla 2
    # ---------------------------------------------------------

    diccionario_de_reemplazos["<<tabla_transmision>>"] = {
        "tabla": tabla3,
        "estilos_de_tabla": estilos_tabla_2,
        "opciones_de_tabla": opciones_tabla_2}

    # ---------------------------------------------------------
    # Título tabla 2
    # ---------------------------------------------------------

    fecha_inicio= get_dia_de_liberacion(df_porcentajes= df_porcentajes)
    fecha_final_vigencia = get_fecha_final_vigencia(df_datos_despliegue = df_datos_despliegue)
    
    diccionario_de_reemplazos["<<titulo_tabla_2>>"] = {
        "texto": (
            "Porcentaje de datos transmitidos y visualizados por variable en "
            "cada una de las sondas oceanográficas liberadas; periodo del "
            f"{fecha_inicio} al {fecha_final_vigencia}.")
    }
    # ---------------------------------------------------------
    # Referencia tabla 2
    # ---------------------------------------------------------

    diccionario_de_reemplazos["<<ref_tabla_2>>"] = [
        "tabla_2"]

    # =========================================================
    # TABLA 3 - PORCENTAJE DE NO VISUALIZACIÓN
    # =========================================================

    df_expanded = (
        df_porcentajes
        .loc[
            df_porcentajes.index.repeat(
                len(variables))].copy().reset_index(drop=True))

    df_expanded["variable"] = (
        variables * len(df_porcentajes))

    df_expanded["porcentaje_no_visualizado"] = (
        100
        - df_expanded["porcentaje_de_datos_recibidos"])

    df_expanded["porcentaje_no_visualizado"] = (
        df_expanded[
            "porcentaje_no_visualizado"
        ].round(2))

    # ---------------------------------------------------------
    # DataFrame tabla 3
    # ---------------------------------------------------------

    tabla3 = df_expanded[
        [
            "serial_de_sonda",
            "variable",
            "cantidad_de_datos_esperados",
            "cantidad_de_datos_recibidos",
            "porcentaje_no_visualizado"]].copy()

    # ---------------------------------------------------------
    # Configuración tabla 3
    # ---------------------------------------------------------

    opciones_tabla_3 = OpcionesTabla()
    estilos_tabla_3 = EstilosTabla(doc)

    estilos_tabla_3.set_estilo_por_defecto(
        "texto_tablas_centrado")

    opciones_tabla_3.set_detectar_merge(True)

    opciones_tabla_3.set_columnas_para_merge(
        [0, 1])

    estilos_tabla_3.set_estilo_de_columna(
        1,
        "texto_tablas_centrado")

    estilos_tabla_3.set_estilo_de_columna(
        2,
        "texto_tablas_centrado")

    estilos_tabla_3.set_estilo_de_columna(
        3,
        "texto_tablas_centrado")

    estilos_tabla_3.set_estilo_de_columna(
        4,
        "texto_tablas_centrado")

    # ---------------------------------------------------------
    # Registrar tabla 3
    # ---------------------------------------------------------

    diccionario_de_reemplazos["<<tabla_no_visualizacion>>"] = {
        "tabla": tabla3,
        "estilos_de_tabla": estilos_tabla_3,
        "opciones_de_tabla": opciones_tabla_3}

    # ---------------------------------------------------------
    # Título tabla 3
    # ---------------------------------------------------------

    diccionario_de_reemplazos["<<titulo_tabla_3>>"] = {
        "texto": (
            "Porcentaje de datos no visualizados en "
            f"los sensores de las sondas oceanográficas liberadas, periodo del {fecha_inicio} al {fecha_final_vigencia}.")
    }
    # ---------------------------------------------------------
    # Referencia tabla 3
    # ---------------------------------------------------------
    diccionario_de_reemplazos["<<ref_tabla_3>>"] = [
        "tabla_3"]

    print("Datos de las tablas 1, 2 y 3 preparados correctamente.")
