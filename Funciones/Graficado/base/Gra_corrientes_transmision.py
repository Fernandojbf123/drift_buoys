####################### N O  T O C A R ############################################
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

from Funciones.Graficado.Gra_asignar_ylim import Gra_asignar_ylim
from Funciones.Graficado.Gra_serie_de_tiempo import Gra_serie_de_tiempo
from Funciones.Graficado.GraFormatoFecha import GraFormatoFecha
from Funciones.Graficado.Gra_calcular_xticks import Gra_calcular_xticks

from Funciones.Utils.utils_get_config_vars import *
from Funciones.Utils.utils_get_vars_dic  import *
##################################################################################
 
def Gra_corrientes_transmision(dataFrame:pd.DataFrame, NS_sonda:str, tspan_column=None) -> tuple[Figure, str]:  
    """
    Descripción:
        Genera gráficos de transmision para datos del ADCP con 10 subplots organizados en 5 filas × 2 columnas.
        Columna izquierda: series de tiempo (Temp, u, v, Rap, Dir)
        Columna derecha: histogramas correspondientes
       
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

    origen_de_los_datos = get_origen_de_los_datos()

    tipo_de_letra = get_tipo_letra()
    tamanio_de_letra = get_tamanio_letra()
    titlesize = tamanio_de_letra + 6
    yticksize = tamanio_de_letra + 3

    numero_de_bins_histograma = get_numero_bins_histograma()
       
    # Crear figura con 5 filas × 1 columna
    fig, axs = plt.subplots(nrows=len(get_variables_graficar()), figsize=(15, 10))
    
    # Variables a graficar
    var_names = get_variables_graficar()
    ylabels = get_ylabels(var_names)
    variables = list(zip(var_names, ylabels))

    # Obtener tspan (el eje X - en formato pd.DatetimeIndex)
    tspan = dataFrame[tspan_column] if tspan_column else dataFrame.index
    # Cambiar tspan a formato mdates
    tspan_num = mdates.date2num(tspan)
    
    # Calcular límites del eje X ¡
    xlim_min, xlim_max, xticks_finales = Gra_calcular_xticks(tspan, n_ticks=5)
    # Ajustar el formato del eje X para que quede dia/mes/año (eg. 01/Dic/2025)
    formateador = FuncFormatter(GraFormatoFecha)
    
    # Iterar sobre las filas según la cantidad de variables a graficar
    for idx, (var_name, ylabel) in enumerate(variables):
        # Subplot izquierdo: Serie de tiempo
        ax_serie = axs[idx]
        data = dataFrame[var_name].dropna()
        
        # Graficar serie de tiempo
        Gra_serie_de_tiempo(dataFrame=dataFrame, var_name=var_name, tspan=tspan_num, ax=ax_serie)
        
        # Configurar límites y etiquetas
        ax_serie = Gra_asignar_ylim(data, var_name, ax_serie, hist=False)
        
        ax_serie.set_ylabel(ylabel, font=tipo_de_letra, fontweight='bold', fontsize=yticksize)
        ax_serie.tick_params(axis='y', labelsize=yticksize)

        ax_serie.set_xlim([xlim_min, xlim_max])
        ax_serie.set_xticks(xticks_finales)
        ax_serie.tick_params(axis='x', labelsize=yticksize)
        
        ax_serie.grid(True, color='gray', linestyle='-', linewidth=0.4)
        ax_serie.set_axisbelow(True)
        
        # Quitar etiquetas X excepto en la última fila
        ax_serie.tick_params(labelbottom=False)
        if idx == len(variables) - 1: # solo el último subplot tiene etiquetas del eje X
            ax_serie.tick_params(labelbottom=True)
            ax_serie.xaxis.set_major_formatter(formateador)
            for label in ax_serie.get_xticklabels():
                label.set_fontweight('bold')
    

    # Alinear etiquetas del eje Y
    fig.align_ylabels(axs[:])

    # Preparar el título de la figura y de guardado
    t0str = tspan.min().strftime('%Y%m%d')
    tEstr = tspan.max().strftime('%Y%m%d')
    strDeFechas = str(f"{t0str}-{tEstr}")
    tituloBase = str(f"SONDA OCEANOGRÁFICA-NS-{NS_sonda}-{origen_de_los_datos}-{strDeFechas}")
    tituloFig = tituloBase
    fig.suptitle(tituloFig, font=tipo_de_letra, fontweight='bold', fontsize=titlesize, y=0.98)
    nombre_de_figura = tituloFig.replace(" ", "_").replace("-", "_").replace("Á", "A")

    # Ajustar layout
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.3, hspace=0.15)

    plt.close(fig)
    return fig, nombre_de_figura