import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from global_config.manager_diccionario_variables import get_ylabels
from procesado_datos.config_modulo.ProcesadoConfig import ProcesadoConfig
from procesado_datos.services.Graficado.base.Gra_serie_de_tiempo import graficar_serie_de_tiempo
from procesado_datos.services.Graficado.base.Gra_dar_formato_a_figuras import *
from procesado_datos.services.Graficado.base.Gra_series_de_tiempo_telemetria import Gra_series_de_tiempo_telemetria
from procesado_datos.services.Utils.utilidades import *
################################################################################


def graficar_series_laboratorio_y_guardar(datos: dict, 
                                          mostrar_figura:bool=False, 
                                          ruta_a_la_carpeta_de_guardado: str = "",
                                          config: ProcesadoConfig | None = None) -> None:
    """
    Descripción:
        Función envoltorio que recorre un diccionario de DataFrames (uno por sonda)
        y genera una figura con 10 subplots para cada sonda:
        - 5 series de tiempo (izquierda): Temp, u, v, Rap, Dir
        - 5 histogramas (derecha): uno por cada serie de tiempo

    Parámetros:
        datos: dict

    Retorna:
        Fig
        Genera y muestra las figuras para cada sonda en el diccionario.

    Ejemplo:
        graficar_series_laboratorio_y_guardar(datos)

    Funciones auxiliares:
        - cargar_diccionario_pickle
        - Gra_series_de_tiempo_telemetria
    """
    # Cargar datos procesados

    seriales_de_sondas = list(datos.keys())
    # Recorrer cada sonda en el diccionario
    
    var_name = ["voltaje"]
    ylabel = get_ylabels(var_name)[0]
    
    for serial, df in datos.items():
        
        
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 2))
        axes = np.atleast_1d(axes)  # Asegurar que axes es siempre un array 1D
        
        ## Paso 2. # Graficar una serie de tiempo por cada axes
        tspan = pd.to_datetime(df["fecha"], format = "%Y-%m-%dT%H:%M:%S.%fZ")
        tspan_num = mdates.date2num(tspan)
  
        ax = graficar_serie_de_tiempo(
                axe=axes[0],
                datos=df,
                var_name="volt",
                tspan_num = tspan_num,
        )
            
        propiedades_del_axe = {
            "obj_axes": ax,  # axis de matplotlib
            "var_name":"voltaje",
            "var_value": df["volt"],
            "tspan": tspan,
            "ylabel":ylabel,
            "xlabel": '',
            "is_xticks_on": True,

        }
        # Paso 3. Dar formato al axe
        dar_formato_al_axe(propiedades_del_axe, config)
        # ax.legend([f"{serial}"], loc="upper left", fontsize=12, frameon=True)
        ax.set_ylim(39, 45)
    
        fecha_inicial_str = tspan.iloc[0].strftime('%Y%m%d')
        fecha_final_str = tspan.iloc[-1].strftime('%Y%m%d')
        
        titulo_figura = f"SONDA OCEANOGRÁFICA NS-{serial}-REALT-{fecha_inicial_str}-{fecha_final_str}"
        propiedades_de_la_figura = {
                "fig": fig,
                "axes": axes,
                "tspan": tspan,
                "titulo_de_figura": titulo_figura,
                "NS_sonda": "",
        }
        
        # Paso 5. Dar formato a la figura
        dar_formato_a_figura_de_series_de_tiempo(propiedades_de_la_figura, config)
    
        # Mostrar o cerrar la figura según el parámetro
        if mostrar_figura:
            plt.show()
        else:
            plt.close(fig)
        
        # Guardar figura
        nombre_del_archivo = f"pruebas_baterias_{serial}"
        guardar_figura(figura=fig,
                        ruta_a_carpeta = ruta_a_la_carpeta_de_guardado,
                        nombre_archivo = nombre_del_archivo,
                        formato = config.formato_de_figuras,
                        resolucion = config.resolucion_de_figuras)
