####################### N O  T O C A R ############################################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure

from Funciones.Graficado.base.Gra_dar_formato_a_figuras import *
from Funciones.Graficado.base.Gra_serie_de_tiempo import graficar_serie_de_tiempo

from Funciones.Utils.utils_get_config_vars import *
from Funciones.Utils.utils_get_vars_dic import *
##################################################################################


def Gra_series_de_tiempo_telemetria(dataFrame: pd.DataFrame, 
                                    NS_sonda: str, 
                                    tspan_column=None,
                                    mostrar_figura:bool=False) -> tuple[Figure, str]:
    """
    Descripción:
        Genera gráficos de transmision para datos del ADCP con hasta 5 subplots organizados en 5 filas.
        series de tiempo (Temp, u, v, Rap, Dir)
    Parámetros:
        dataFrame : pd.DataFrame
            DataFrame con los datos de entrada. Debe contener las columnas:
            'temperatura', 'velocidad_u', 'velocidad_v', 'rapidez', 'direccion'
            El índice debe ser de tipo datetime.

        NS_sonda : str
            Número de serie de la sonda para el título.

    Retorna:
        fig : Figure
            Objeto Figure que contiene los 10 subplots.
        tituloFig : str
            Título base utilizado para la figura.

    Ejemplo: 
        fig, titulo = Gra_corrientes_transmision(df, "123456")

    Funciones auxiliares: 
        -Gra_serie_de_tiempo
        -GraFormatoFecha
        -GraTicks_corregido
        -Gra_calcular_ylim

    Categoría:
        Gráficos-base 
    """

    ## Paso 1. Crear obj figura y array de objs axes
    fig, axes = plt.subplots(nrows=len(get_variables_graficar()), figsize=(15, 10))
    axes = np.atleast_1d(axes)  # Asegurar que axes es siempre un array 1D
    
    # Variables a graficar
    var_names = get_variables_graficar()
    ylabels = get_ylabels(var_names)
    variables = list(zip(var_names, ylabels))
    
    # Eliminar los nans del dataframe
    df = dataFrame.dropna(subset="tspan_rounded").copy()
    
    ## Paso 2. # Graficar una serie de tiempo por cada axes
    tspan = df[tspan_column] if tspan_column else df.index
    tspan_num = mdates.date2num(tspan)
        
    for idx, (var_name, ylabel) in enumerate(variables):
        ax = axes[idx]
        ax = graficar_serie_de_tiempo(
            axe=ax,
            datos=df,
            var_name=var_name,
            tspan_num = tspan_num,
        )
        
        propiedades_del_axe = {
            "obj_axes": ax,  # axis de matplotlib
            "var_name":var_name,
            "var_value": df[var_name],
            "tspan": tspan,
            "ylabel":ylabel,
            "xlabel": '',
            "is_xticks_on": True if idx == len(variables) - 1 else False,

        }
        # Paso 3. Dar formato al axe
        dar_formato_al_axe(propiedades_del_axe)
    
    # Paso 4. Crear título de la figura y nombre de guardado
    titulo_de_figura, nombre_de_guardado = crear_titulo_de_figura_serie_de_tiempo_y_nombre_de_guardado(tspan=tspan, NS_sonda=NS_sonda)
    
    propiedades_de_la_figura = {
        "fig": fig,
        "axes": axes,
        "tspan": tspan,
        "titulo_de_figura": titulo_de_figura,
        "NS_sonda": NS_sonda,
    }
    
    # Paso 5. Dar formato a la figura
    dar_formato_a_figura_de_series_de_tiempo(propiedades_de_la_figura)

    # Mostrar o cerrar la figura según el parámetro
    if mostrar_figura:
        plt.show()
    else:
        plt.close(fig)
        
    return fig, nombre_de_guardado
