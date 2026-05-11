import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv

from services.Graficado.base.Gra_serie_de_tiempo import graficar_serie_de_tiempo
from services.Graficado.base.Gra_dar_formato_a_figuras import *
from services.Graficado.base.Gra_series_de_tiempo_telemetria import Gra_series_de_tiempo_telemetria
from configs.manager_configuracion import *
from services.Utils.utilidades import *
################################################################################


def graficar_series_laboratorio_y_guardar(mostrar_figura:bool=False) -> None:
    """
    Descripción:
        Función envoltorio que recorre un diccionario de DataFrames (uno por sonda)
        y genera una figura con 10 subplots para cada sonda:
        - 5 series de tiempo (izquierda): Temp, u, v, Rap, Dir
        - 5 histogramas (derecha): uno por cada serie de tiempo

    Parámetros:
        Ninguno (lee desde configuración general)

    Retorna:
        None
        Genera y muestra las figuras para cada sonda en el diccionario.

    Ejemplo:
        graficar_series_y_guardar()

    Funciones auxiliares:
        - cargar_diccionario_pickle
        - Gra_series_de_tiempo_telemetria
    """
    # Cargar datos procesados
    ruta_a_la_carpeta_de_datos_procesados = crear_ruta_a_carpeta(get_carpeta_guardado_datos_procesados())
    nombre_del_archivo_de_datos_procesados = "datos_interpolados"#get_nombre_archivo_datos_procesados()
    ruta_de_archivo = os.path.join(ruta_a_la_carpeta_de_datos_procesados, nombre_del_archivo_de_datos_procesados)

    datos = cargar_diccionario_pickle(ruta_de_archivo)

    seriales_de_sondas = get_seriales_sondas()
    # Recorrer cada sonda en el diccionario
    
    ## Paso 1. Crear obj figura y array de objs axes
    def tamanio_de_figura(cantidad_de_vars = len(datos)):
        output = cantidad_de_vars * 2
        return (15,output)
    
    
    fig, axes = plt.subplots(nrows=len(datos), ncols=1, figsize=tamanio_de_figura(len(datos))) 
    axes = np.atleast_1d(axes)  # Asegurar que axes es siempre un array 1D
    
    var_name = ["voltaje"]
    ylabel = get_ylabels(var_name)[0]
    
    for idx, serial in enumerate(seriales_de_sondas):
        
        df = datos[serial]
        
        ## Paso 2. # Graficar una serie de tiempo por cada axes
        tspan = df["tspan_rounded"]
        tspan_num = mdates.date2num(tspan)
  
        ax = graficar_serie_de_tiempo(
                axe=axes[idx],
                datos=df,
                var_name="voltaje",
                tspan_num = tspan_num,
        )
            
        propiedades_del_axe = {
            "obj_axes": ax,  # axis de matplotlib
            "var_name":"voltaje",
            "var_value": df["voltaje"],
            "tspan": tspan,
            "ylabel":ylabel,
            "xlabel": '',
            "is_xticks_on": True if idx == len(seriales_de_sondas) - 1 else False,

        }
        # Paso 3. Dar formato al axe
        dar_formato_al_axe(propiedades_del_axe)
        ax.legend([f"{serial}"], loc="upper left", fontsize=12, frameon=True)
        ax.set_ylim(39, 45)
    
    propiedades_de_la_figura = {
            "fig": fig,
            "axes": axes,
            "tspan": tspan,
            "titulo_de_figura": "Pruebas de voltaje de laboratorio",
            "NS_sonda": "",
    }
        
    # Paso 5. Dar formato a la figura
    dar_formato_a_figura_de_series_de_tiempo(propiedades_de_la_figura)
    
    # Mostrar o cerrar la figura según el parámetro
    if mostrar_figura:
        plt.show()
    else:
        plt.close(fig)
        
    # Guardar figura
    guardar_figura(figura=fig,
                    ruta_a_carpeta=crear_ruta_a_carpeta(get_carpeta_guardado_figuras()),
                    nombre_archivo="pruebas_de_voltaje_laboratorio",
                    formato=get_formato_figuras(),
                    resolucion=get_resolucion_de_figuras())
