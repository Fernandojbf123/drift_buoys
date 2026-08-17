"""Punto de entrada para procesar los datos de transmisión.

Se puede ejecutar de dos formas desde la raíz del proyecto:

    python procesado_datos/transmision/main_transmision_pruba.py
    python -m procesado_datos.transmision.main_transmision_pruba

También puede importarse desde un standalone::

    from procesado_datos.transmision.main_transmision_pruba import main
    main()
"""

import copy
import os
import sys
from pathlib import Path


# Permite ejecutar este archivo directamente, además de como módulo.
ROOT_PATH = Path(__file__).resolve().parents[2]
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig
from procesado_datos.config_modulo.config_procesado import config_modulo_procesado
from procesado_datos.services.Carga import cargar_datos_csv as carga
from procesado_datos.services.Correctores.corrector_utils import (
    eliminar_datos_espurios,
    reemplazar_datos_de_rapidez_distancia_y_direccion_de_primera_medicion_por_null,
)
from procesado_datos.services.Graficado.graficar_mapa_de_posiciones import (
    graficar_mapa_de_posiciones,
)
from procesado_datos.services.Graficado.graficar_series_y_guardar import (
    graficar_series_y_guardar,
)
from procesado_datos.services.Utils.excel_a_png import csv_a_png
from procesado_datos.services.Utils.utilidades import (
    calcular_porcentaje_de_datos_recibidos,
    guardar_diccionario_como_pickle,
    guardar_porcentajes_en_excel,
)
from procesado_datos.transmision.configs.configuracion_transmision import (
    config_transmision,
)


def crear_configuracion() -> ProcesadoConfig:
    """Construye la configuración común y específica de transmisión."""
    return ProcesadoConfig.from_sources(
        config_modulo_procesado,
        config_transmision,
    )


def main(config: ProcesadoConfig | None = None) -> dict:
    """Ejecuta el flujo completo de transmisión y devuelve los datos finales.

    El parámetro ``config`` permite llamarlo desde otro standalone con una
    configuración ya creada; si se omite, se carga la configuración estándar.
    """
    if config is None:
        config = crear_configuracion()

    fecha_del_estudio = config.convertir_a_pd_datetime(
        "fecha_del_estudio", formato="%Y-%m-%d"
    )
    carpeta_del_estudio = f"{fecha_del_estudio.year:04d}{fecha_del_estudio.month:02d}"
    ruta_a_la_carpeta_de_guardado = os.path.join(
        config.carpeta_de_guardado_de_datos_procesados,
        carpeta_del_estudio,
    )
    Path(ruta_a_la_carpeta_de_guardado).mkdir(parents=True, exist_ok=True)

    rutas_de_sondas, seriales_encontrados = carga.buscar_nombre_de_archivo_de_sonda(config)
    diccionario_de_datos_de_sondas = carga.cargar_datos_de_sonda(
        rutas_de_sondas, seriales_encontrados
    )
    diccionario_de_datos_de_sondas = (
        reemplazar_datos_de_rapidez_distancia_y_direccion_de_primera_medicion_por_null(
            diccionario_de_datos_de_sondas
        )
    )

    # Guarda la versión para la página web con sus nombres de columna esperados.
    nombres_de_columnas_de_pagina_web = [
        "fecha", "latitud", "logitud", "speed", "distance", "direction",
        "direction_gen", "temp", "volt",
    ]
    dict_guardado = copy.deepcopy(diccionario_de_datos_de_sondas)
    rutas_de_archivos_csv_corregidos = []
    for serial, datos in dict_guardado.items():
        for columna in ("rap_corriente", "distancia", "dir_corriente", "dir_corriente_texto"):
            if columna in datos.columns:
                datos[columna] = datos[columna].astype(str)
                datos.loc[datos.index[0], columna] = (
                    str(datos.loc[datos.index[0], columna]).replace("nan", "Null")
                )

        if len(datos.columns) != len(nombres_de_columnas_de_pagina_web):
            raise ValueError(
                f"La sonda {serial} tiene {len(datos.columns)} columnas; "
                f"se esperaban {len(nombres_de_columnas_de_pagina_web)} para el CSV web."
            )
        datos.columns = nombres_de_columnas_de_pagina_web
        ruta_a_guardar = os.path.join(
            ruta_a_la_carpeta_de_guardado, f"datos_Localizacion_{serial}.csv"
        )
        datos.to_csv(ruta_a_guardar, index=False)
        rutas_de_archivos_csv_corregidos.append(ruta_a_guardar)

    diccionario_de_sondas_en_fechas = carga.seleccionar_rango_de_fechas(
        diccionario=diccionario_de_datos_de_sondas,
        buscar_fechas_anteriores_al_estudio=False,
        config=config,
    )
    datos_de_sondas_sin_duplicados = carga.buscar_y_eliminar_duplicados(
        diccionario_de_sondas_en_fechas
    )
    datos_ordenados = carga.ordernar_datos_por_fecha(datos_de_sondas_sin_duplicados)

    for serial in seriales_encontrados:
        if serial in datos_ordenados:
            datos_ordenados[serial]["tspan_rounded"] = datos_ordenados[serial]["tspan_de_envio"]

    datos_finales = eliminar_datos_espurios(datos_ordenados)
    datos_finales = carga.agregar_componentes_de_la_velocidad(datos_finales)

    guardar_diccionario_como_pickle(
        diccionario=datos_finales,
        ruta=ruta_a_la_carpeta_de_guardado,
        nombre_archivo=config.nombre_del_archivo_de_datos_procesados,
    )
    tabla_de_porcentajes = calcular_porcentaje_de_datos_recibidos(datos_finales, config)
    guardar_porcentajes_en_excel(
        data=tabla_de_porcentajes,
        ruta=ruta_a_la_carpeta_de_guardado,
        nombre_de_archivo=config.nombre_del_excel_de_porcentajes,
    )
    graficar_series_y_guardar(
        datos=datos_finales,
        ruta_a_carpeta_de_guardado=ruta_a_la_carpeta_de_guardado,
        mostrar_figura=False,
        config=config,
    )
    graficar_mapa_de_posiciones(
        datos=datos_finales,
        ruta_a_la_carpeta_de_guardado=ruta_a_la_carpeta_de_guardado,
        mostrar_figura=False,
        config=config,
    )

    if rutas_de_archivos_csv_corregidos:
        csv_a_png(
            rutas_de_archivos_csv_corregidos[0],
            carpeta_salida=ruta_a_la_carpeta_de_guardado,
            max_filas=20,
            nombre_salida="mensaje.png",
        )
        print("Se ha guardado el PNG del mensaje de transmisión.")

    return datos_finales


if __name__ == "__main__":
    main()
