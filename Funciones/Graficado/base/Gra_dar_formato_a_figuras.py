"""Archivo con funciones para dar formato a la figura
    Contiene: 
    - Formatos de axes
    - Formatos de fechas en eje X
    - Formatos de eje Y
    
"""
############################### IMPORTS NO TOCAR ##############################
import locale
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.axes import Axes
from matplotlib.ticker import MaxNLocator

from Funciones.Utils.utils_get_config_vars import *

# Configurar locale para español (compatible con Windows)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Unix/macOS
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')  # Windows alternativa
    except:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain')  # Windows
##################################################################################
def dar_formato_a_figura_de_series_de_tiempo(propiedades: dict) -> None:
    """
    Descripción:
        Aplica formato general a una figura de matplotlib con múltiples subplots de series de tiempo.
        Alinea las etiquetas del eje Y, añade título superior, y ajusta márgenes y espacios
        entre subplots para una presentación óptima.

    Parámetros:
        propiedades (dict): Diccionario con las propiedades de formato de la figura.
            - "fig" (matplotlib.figure.Figure): Objeto Figure de matplotlib a formatear (requerido).
            - "axes" (list o array): Lista de objetos Axes de los subplots (requerido).
            - "titulo_de_figura" (str, opcional): Título principal de la figura. Por defecto: ''.

    Retorna:
        None: Modifica el objeto Figure directamente (in-place).

    Ejemplo:
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> import pandas as pd
        >>> # Crear figura con 3 subplots
        >>> fig, axes = plt.subplots(3, 1, figsize=(10, 8))
        >>> # Graficar datos en cada subplot
        >>> for i, ax in enumerate(axes):
        ...     x = pd.date_range('2025-01-01', periods=100, freq='H')
        ...     y = np.random.rand(100) * (i + 1)
        ...     ax.plot(x, y)
        ...     ax.set_ylabel(f'Variable {i+1}')
        >>> # Aplicar formato a la figura completa
        >>> propiedades = {
        ...     "fig": fig,
        ...     "axes": axes,
        ...     "titulo_de_figura": "Series de Tiempo - Datos Oceanográficos"
        ... }
        >>> dar_formato_a_figura_de_series_de_tiempo(propiedades)
        >>> plt.show()

    Notas:
        - Alinea automáticamente todas las etiquetas del eje Y de los subplots.
        - El título se posiciona en y=0.98 de la figura.
        - Los espacios horizontales (wspace) se ajustan a 0.3.
        - Los espacios verticales (hspace) se ajustan a 0.15.
        - El tamaño de fuente del título es 6 puntos mayor que el tamaño base.

    Funciones auxiliares:
        - get_tipo_letra(): Obtiene el tipo de fuente configurado
        - get_tamanio_de_letra(): Obtiene el tamaño base de fuente

    Categoría:
        Gráficos
    """
    fig = propiedades.get("fig", None)
    axes = propiedades.get("axes", None)
    titulo_de_figura = propiedades.get("titulo_de_figura", "")
    tipo_de_letra = get_tipo_letra()
    titlesize = get_tamanio_de_letra() + 6
    
    # Alinear etiquetas del eje Y
    fig.align_ylabels(axes[:])
    # Poner título
    fig.suptitle(titulo_de_figura, font=tipo_de_letra, fontweight='bold', fontsize=titlesize, y=0.98)
    # Ajustar layout
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.3, hspace=0.15)


def dar_formato_al_axe(propiedades_del_axe: dict) -> None:
    """
    Descripción:
        Aplica formato completo a un eje (axis) de matplotlib para series de tiempo.
        Configura límites, etiquetas, grid, ticks del eje X (fechas) y eje Y (valores),
        incluyendo eje secundario para variables de dirección (puntos cardinales).

    Parámetros:
        propiedades_del_axe (dict): Diccionario con las propiedades del eje a formatear.
            - "obj_axes" (matplotlib.axes.Axes): Objeto axis de matplotlib (requerido).
            - "var_name" (str): Nombre de la variable a graficar (ej: 'Hs', 'dir_corriente').
            - "var_value" (array-like): Valores de la variable para calcular límites del eje Y.
            - "tspan" (pd.DatetimeIndex): Índice de fechas para configurar el eje X.
            - "ylabel" (str, opcional): Etiqueta del eje Y. Por defecto: ''.
            - "xlabel" (str, opcional): Etiqueta del eje X. Por defecto: ''.
            - "is_xticks_on" (bool, opcional): Si True, muestra etiquetas en el eje X. Por defecto: False.

    Retorna:
        None: Modifica el objeto Axes directamente (in-place).

    Ejemplo:
        >>> import matplotlib.pyplot as plt
        >>> import pandas as pd
        >>> fig, ax = plt.subplots()
        >>> tspan = pd.date_range('2025-01-01', '2025-01-10', freq='H')
        >>> var_value = np.random.rand(len(tspan)) * 2.5
        >>> propiedades = {
        ...     "obj_axes": ax,
        ...     "var_name": 'Hs',
        ...     "var_value": var_value,
        ...     "tspan": tspan,
        ...     "ylabel": 'Altura de ola (m)',
        ...     "is_xticks_on": True
        ... }
        >>> dar_formato_al_axe(propiedades)

    Funciones auxiliares:
        - Gra_calcular_xticks: Calcula ticks y límites del eje X
        - Gra_asignar_ylim: Calcula límites y ticks del eje Y
        - Gra_Formato_Fecha_ddmmyyyy: Formateador de fechas (días)
        - Gra_Formato_Fecha_ddmmyyyy_HH: Formateador de fechas (horas)
        
    Categoría:
        Gráficos
    """
    # Extraer propiedades con valores por defecto si no se proporcionan
    obj_axes = propiedades_del_axe.get("obj_axes", None)
    var_name = propiedades_del_axe.get("var_name", '')
    var_value = propiedades_del_axe.get("var_value", None)
    tspan = propiedades_del_axe.get("tspan", None)

    ylabel = propiedades_del_axe.get("ylabel", '') 
    xlabel = propiedades_del_axe.get("xlabel", '') 
    is_xticks_on = propiedades_del_axe.get("is_xticks_on", False)
    
    tipo_de_letra = get_tipo_letra()
    tamanio_de_letra = get_tamanio_de_letra()
    ylabelsize = tamanio_de_letra
    yticksize = tamanio_de_letra
    xlabelsize = tamanio_de_letra
    xticksize = tamanio_de_letra
        
    ## Grid
    obj_axes.grid(True, which='both', linestyle='--', color='gray', alpha=0.5)
    obj_axes.set_axisbelow(True)
    

    ## Atributos del eje Y
    # Etiqueta del eje Y
    obj_axes.set_ylabel(ylabel, fontname=tipo_de_letra, fontweight='bold', fontsize=ylabelsize)
    # Calcular ylim y yticks; luego asignar los valores calculados; y si es dirección agrega el eje secundario (por eso se necesita ylabelsize)
    _ , obj_axes_2 = asignar_ylim(obj_axes = obj_axes, var_value = var_value, var_name = var_name, ylabelsize=yticksize) 
    
    # Formato de los ticks del eje Y
    for label in obj_axes.get_yticklabels():
        label.set_fontname(tipo_de_letra)
        label.set_fontsize(yticksize)
        label.set_fontweight('bold')
        
    if obj_axes_2 is not None:
        for label in obj_axes_2.get_yticklabels():
            label.set_fontname(tipo_de_letra)
            label.set_fontsize(yticksize)
            label.set_fontweight('bold')
        
    ## Atributos del eje X
    # Etiqueta del eje X (por lo general, se deja vacía)
    obj_axes.set_xlabel(xlabel, fontname=tipo_de_letra, fontweight='bold', fontsize=xlabelsize)

    # Calcular xlim y xticks
    xlim, xticks_finales, xticks_format = calcular_xticks(tspan = tspan, n_ticks=5)
    # Asignar los xticks calculados
    obj_axes.set_xticks(xticks_finales)
    
    # Fijar Xlim
    obj_axes.set_xlim(xlim)
    
    # Tamañoy tipo de letra de los ticks del eje X (si es que aplica)
    obj_axes.tick_params(labelbottom=False)
    if is_xticks_on:  # solo el último subplot tiene etiquetas del eje X
        # Formatear el eje X como dd/mmm/yyyy o dd/mmm/yyyy HH:00
        obj_axes.tick_params(labelbottom=True)
        obj_axes.xaxis.set_major_formatter(formato_fecha_ddmmyyyy) # Por defecto formato de días
        if xticks_format == "hours":
            obj_axes.xaxis.set_major_formatter(formato_fecha_ddmmyyyy_HH)    
      
        for label in obj_axes.get_xticklabels():    
            label.set_fontname(tipo_de_letra)
            label.set_fontsize(xticksize)
            label.set_fontweight('bold')

    
#######################
def calcular_xticks(tspan: pd.DatetimeIndex, n_ticks:int =5)-> tuple:
    """
    Descripción:
        Calcula los límites y ticks óptimos para el eje X de un gráfico de series de tiempo.
        Ajusta automáticamente la frecuencia de los ticks (por día o por hora) según el
        rango temporal de los datos.

    Parámetros:
        tspan (pd.DatetimeIndex): Índice de fechas que representa el rango temporal de los datos.
        n_ticks (int, opcional): Número deseado de ticks en el eje X. Por defecto: 5.

    Retorna:
        tuple: Tupla con tres elementos:
            - xlim (tuple): Límites del eje X (fecha_inicial, fecha_final) con padding.
            - ticks (pd.DatetimeIndex): Array de fechas para los ticks del eje X.
            - formato_ticks (str): Tipo de formato ('days' o 'hours') según el rango temporal.

    Ejemplo:
        >>> import pandas as pd
        >>> tspan = pd.date_range('2025-01-15', '2025-01-20', freq='H')
        >>> xlim, ticks, formato = Gra_calcular_xticks(tspan, n_ticks=5)
        >>> print(f"Límites: {xlim}")
        >>> print(f"Formato: {formato}")
        >>> print(f"Número de ticks: {len(ticks)}")
        Límites: (Timestamp('2025-01-14'), Timestamp('2025-01-21'))
        Formato: days
        Número de ticks: 5

    Notas:
        - Si el rango es >= 6 días: ticks diarios con padding de 1 día
        - Si el rango es 3-5 días: ticks diarios con padding de 2 horas
        - Si el rango es <= 2 días: ticks por hora con padding de 1 hora
        
    Funciones auxiliares:
        Ninguna
        
    Categoría:
        Gráficos
    """
    fecha_inicial = tspan.min()
    fecha_final = tspan.max()
    
    diferencia = fecha_final.normalize() - fecha_inicial.normalize() + pd.Timedelta(days=1)
    
    if diferencia.days >=6:
        # ticks cada día
        ticks = pd.date_range(
            start=fecha_inicial.normalize(),
            end=fecha_final.normalize(),
            freq='D'
        )
        
        xlim = (fecha_inicial.normalize() - pd.Timedelta(days=1), fecha_final + pd.Timedelta(days=1))
        formato_ticks = "days"
    
    
    elif diferencia.days < 6  and diferencia.days >2:
        # ticks cada día
        ticks = pd.date_range(
            start=fecha_inicial.normalize(),
            end=fecha_final.normalize(),
            freq='D'
        )
        n_ticks = diferencia.days
        
        xlim = (fecha_inicial.normalize() - pd.Timedelta(hours=2), fecha_final + pd.Timedelta(hours=2))
        formato_ticks = "days"
    
    elif diferencia.days <= 2:
        ticks = pd.date_range(
            start=fecha_inicial,
            end=fecha_final,
            freq='h'
        )
        
        xlim = (fecha_inicial - pd.Timedelta(hours=1), fecha_final + pd.Timedelta(hours=1)) 
        formato_ticks = "hours"
    
    # seleccionar n_ticks equiespaciados (Deben ser 5 salvo que sea el caso (entre 3 y 4 días))
    if len(ticks) >= n_ticks:
        # 5 índices equiespaciados, siempre el primero y el último
        indices = np.linspace(0, len(ticks)-1, n_ticks, dtype=int)
        ticks = ticks[indices]
            
    return xlim, ticks, formato_ticks


#######################
def formato_fecha_ddmmyyyy_HH(tspan_num: float, pos: int) -> str:
    """
    Descripción:
        Formatea fechas numéricas de Matplotlib a cadena legible en español con
        el formato 'dd/Mes/yyyy:HH:00', incluyendo la hora. Utiliza abreviaturas
        de meses sin punto (ej: 'Ene' en lugar de 'ene.').
        
        Esta función es utilizada como formateador en el eje X para gráficos de
        series temporales con resolución horaria.

    Parámetros:
        tspan_num (float): Valor de fecha en formato numérico de Matplotlib.
        pos (int, opcional): Posición del tick en el eje (requerido por matplotlib.ticker.FuncFormatter,
            pero no se utiliza en la implementación).

    Retorna:
        str: Cadena con la fecha y hora formateada.
       
    Ejemplo:
        >>> from matplotlib.dates import date2num
        >>> import datetime
        >>> fecha = datetime.datetime(2025, 2, 3, 15, 0)
        >>> tspan_num = date2num(fecha)
        >>> Gra_Formato_Fecha_ddmmyyyy_HH(tspan_num)
        '03/Feb/2025:15:00'
        
    Funciones auxiliares:
        Ninguna
    
    Categoría:
        Gráficos
    
    """
    # Diccionario para pasar de algo con punto a sin punto
    meses_sin_punto = {
        'ene.': 'Ene', 'feb.': 'Feb', 'mar.': 'Mar', 'abr.': 'Abr',
        'may.': 'May', 'jun.': 'Jun', 'jul.': 'Jul', 'ago.': 'Ago',
        'sep.': 'Sep', 'oct.': 'Oct', 'nov.': 'Nov', 'dic.': 'Dic'
    }
    
    fecha = mdates.num2date(tspan_num)
    fecha = pd.to_datetime(fecha)  # Convertir a Timestamp de pandas para mejor manejo
    mes = fecha.strftime('%b')  # Obtener mes abreviado
    mes_limpio = meses_sin_punto.get(mes)
    
    return f"{fecha.day:02d}/{mes_limpio}/{fecha.year}:{fecha.hour:02d}:00"



#######################
def formato_fecha_ddmmyyyy(tspan_num: float, pos: int) -> str:
    """
    Descripción:
        Formatea fechas numéricas de Matplotlib a cadena legible en español con
        el formato 'dd/Mes/yyyy'. Utiliza abreviaturas de meses sin punto
        (ej: 'Ene' en lugar de 'ene.').
        
        Esta función es utilizada como formateador en el eje X para gráficos de
        series temporales con resolución diaria.

    Parámetros:
        tspan_num (float): Valor de fecha en formato numérico de Matplotlib.
        pos (int, opcional): Posición del tick en el eje (requerido por matplotlib.ticker.FuncFormatter,
            pero no se utiliza en la implementación).

    Retorna:
        str: Cadena con la fecha formateada.
       
    Ejemplo:
        >>> from matplotlib.dates import date2num
        >>> import datetime
        >>> fecha = datetime.datetime(2025, 2, 3)
        >>> tspan_num = date2num(fecha)
        >>> Gra_Formato_Fecha_ddmmyyyy(tspan_num)
        '03/Feb/2025'
        
    Funciones auxiliares:
        Ninguna
    
    Categoría:
        Gráficos
    
    """
    # Diccionario para pasar de algo con punto a sin punto
    meses_sin_punto = {
        'ene.': 'Ene', 'feb.': 'Feb', 'mar.': 'Mar', 'abr.': 'Abr',
        'may.': 'May', 'jun.': 'Jun', 'jul.': 'Jul', 'ago.': 'Ago',
        'sep.': 'Sep', 'oct.': 'Oct', 'nov.': 'Nov', 'dic.': 'Dic'
    }
    
    fecha = mdates.num2date(tspan_num)
    fecha = pd.to_datetime(fecha)  # Convertir a Timestamp de pandas para mejor manejo
    mes = fecha.strftime('%b')  # Obtener mes abreviado
    mes_limpio = meses_sin_punto.get(mes)
    
    return f"{fecha.day:02d}/{mes_limpio}/{fecha.year}"

####################### 
def asignar_ylim(obj_axes: Axes, var_value: list, var_name: str, ylabelsize: float = 12) -> tuple:
    """
    Descripción: 
        Ajusta automáticamente los límites del eje Y, ticks y etiquetas según el tipo
        de variable y su rango de valores. Crea un eje secundario para variables de
        dirección con puntos cardinales (N, E, S, W).

    Parámetros:
        obj_axes (matplotlib.axes.Axes): Objeto axis de matplotlib donde se ajustarán los límites.
        var_value (array-like): Serie de datos (puede contener NaNs) de la variable a graficar.
        var_name (str): Nombre de la variable para determinar el tipo de ajuste.
            - Variables que inician en 0: "rap_corriente", "Hs", "Hm", "Tp"
            - Variables de temperatura: "temperatura_mar", "temperatura_aire" (límites enteros)
            - Variables de dirección: "dir_corriente" (crea eje secundario con puntos cardinales)
        ylabelsize (float, opcional): Tamaño de fuente para etiquetas del eje Y. Por defecto: 12.

    Retorna:
        tuple: Tupla con dos elementos:
            - obj_axes (matplotlib.axes.Axes): Eje principal con límites y ticks ajustados.
            - obj_axes_2 (matplotlib.axes.Axes o None): Eje secundario (solo para variables de dirección) o None.

    Notas:
        - Se usa 'np.nanmin' y 'np.nanmax' para ignorar valores NaN en los cálculos.
        - Para temperaturas, se fuerzan ticks enteros sin padding.
        - Para variables que inician en 0, el límite inferior es 0.
        - Se agrega 5% de padding vertical para mejor visualización (excepto temperaturas).

    Ejemplo:
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fig, ax = plt.subplots()
        >>> hs_data = np.array([0.5, 1.2, 2.3, 1.8, 1.5])
        >>> ax, ax2 = Gra_asignar_ylim(ax, hs_data, 'Hs', ylabelsize=12)
        >>> print(ax.get_ylim())
        (0.0, 2.415)
        
        >>> # Para variable de dirección
        >>> fig, ax = plt.subplots()
        >>> dir_data = np.array([45, 90, 180, 270, 315])
        >>> ax, ax2 = Gra_asignar_ylim(ax, dir_data, 'dir_corriente', ylabelsize=12)
        >>> print(ax2.get_yticklabels())  # Mostrará: ['N', 'E', 'S', 'W', 'N']

    Funciones auxiliares: 
        Ninguna
    
    Categoría: 
        Gráficos
    """
    obj_axes_2 = None
    mini = np.nanmin(var_value)
    maxi = np.nanmax(var_value)
    # Calcular el rango y el margen
    range_y = maxi - mini
    padding_y = range_y * 0.05  # 5% de margen a cada lado

    # Variables que empiezan en 0
    if var_name.lower() in ["rap_corriente","Hs", "Hm", "Tp"]:
        ylim_min = 0      
        ylim_max = maxi + padding_y

    elif var_name.lower() in ["temperatura_mar","temperatura_aire","voltaje"]:
        # Para temperatura: límites enteros exactos sin padding
        ylim_min = np.floor(mini)-1
        ylim_max = np.ceil(maxi)+1

    else:  # Todas las variables que no sean ["rap_corriente","Hs", "Hm", "Tp"] ni direccion
        ylim_min = mini - padding_y
        ylim_max = maxi + padding_y

    # Variables de direccion
    if var_name in ['dir_corriente']:
        obj_axes.set_ylim([0, 360])
        obj_axes.set_yticks([0, 90, 180, 270, 360])
        # Agregar eje secundario con puntos cardinales
        obj_axes_2 = obj_axes.twinx()
        obj_axes_2.set_ylim([0, 360])
        obj_axes_2.set_yticks([0, 90, 180, 270, 360])
        obj_axes_2.set_yticklabels(['N', 'E', 'S', 'W', 'N'], fontsize= ylabelsize )
        return obj_axes, obj_axes_2

    # Asignar los ejes
    obj_axes.set_ylim(ylim_min, ylim_max)
    
    # Para temperatura, forzar ticks enteros
    if var_name.lower() in ["temperatura_mar","temperatura_aire","voltaje"]:
        obj_axes.yaxis.set_major_locator(MaxNLocator(integer=True))
    else:
        obj_axes.yaxis.set_major_locator(MaxNLocator(nbins=5))
    
    return obj_axes, obj_axes_2


def crear_titulo_de_figura_serie_de_tiempo_y_nombre_de_guardado(tspan: pd.DatetimeIndex, NS_sonda: str) -> tuple:
    origen_de_los_datos = get_origen_de_los_datos()
    # Preparar el título de la figura y de guardado
    t0str = tspan.min().strftime('%Y%m%d')
    tEstr = tspan.max().strftime('%Y%m%d')
    strDeFechas = str(f"{t0str}-{tEstr}")
    titulo_de_figura = str(f"SONDA OCEANOGRÁFICA NS-{NS_sonda}-{origen_de_los_datos}-{strDeFechas}")    
    nombre_de_guardado = titulo_de_figura.replace(" ", "_").replace("-", "_").replace("Á", "A")

    return titulo_de_figura, nombre_de_guardado

######################## MAPA #####################################

def dar_formato_al_mapa(propieadades_de_mapa) -> None:
    """
    Descripción:
        Aplica formato completo a un mapa creado con matplotlib/cartopy.
        Configura títulos, etiquetas de ejes, grid, tamaños de fuente y barra de color
        (colorbar) si se proporciona un objeto mapeable.

    Parámetros:
        propieadades_de_mapa (dict): Diccionario con las propiedades del mapa a formatear.
            - "obj_axes" (matplotlib.axes.Axes): Objeto axis de matplotlib (requerido).
            - "titulo" (str, opcional): Título principal del mapa. Por defecto: ''.
            - "subtitulo" (str, opcional): Subtítulo del mapa. Por defecto: ''.
            - "ylabel" (str, opcional): Etiqueta del eje Y (latitud). Por defecto: ''.
            - "xlabel" (str, opcional): Etiqueta del eje X (longitud). Por defecto: ''.
            - "grid" (bool, opcional): Si True, muestra grid en el mapa. Por defecto: True.
            - "obj_mapeable" (PathCollection o None, opcional): Objeto scatter para colorbar. Por defecto: None.
            - "colorbar_label" (str, opcional): Etiqueta de la barra de color. Por defecto: ''.
            - "colorbar_min" (float, opcional): Valor mínimo de la barra de color. Por defecto: 0.
            - "colorbar_max" (float, opcional): Valor máximo de la barra de color. Por defecto: 1.5.

    Retorna:
        None: Modifica el objeto Axes y la figura directamente (in-place).

    Ejemplo:
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fig, ax = plt.subplots()
        >>> x = np.random.rand(50) * 10 - 75  # longitudes
        >>> y = np.random.rand(50) * 5 + 35   # latitudes
        >>> valores = np.random.rand(50) * 2.5  # altura de ola
        >>> scatter = ax.scatter(x, y, c=valores, cmap='viridis', vmin=0, vmax=2.5)
        >>> propiedades = {
        ...     "obj_axes": ax,
        ...     "titulo": "Mapa de Altura de Ola",
        ...     "subtitulo": "Región del Pacífico",
        ...     "xlabel": "Longitud (°)",
        ...     "ylabel": "Latitud (°)",
        ...     "grid": True,
        ...     "obj_mapeable": scatter,
        ...     "colorbar_label": "Hs (m)",
        ...     "colorbar_min": 0,
        ...     "colorbar_max": 2.5
        ... }
        >>> dar_formato_al_mapa(propiedades)
        >>> plt.show()

    Notas:
        - Si se proporciona tanto título como subtítulo, se muestran en dos líneas.
        - La barra de color solo se crea si obj_mapeable no es None.
        - Los tamaños y tipos de fuente se obtienen de funciones de configuración.
        
    Funciones auxiliares:
        - get_tipo_letra(): Obtiene el tipo de fuente configurado
        - get_tamanio_de_letra(): Obtiene el tamaño base de fuente
        - get_decimales_figuras(): Obtiene decimales para ticks del colorbar
        
    Categoría:
        Gráficos
    """
    # Extraer propiedades con valores por defecto si no se proporcionan
    obj_axes = propieadades_de_mapa.get("obj_axes", None)
    titulo = propieadades_de_mapa.get("titulo", '') 
    subtitulo = propieadades_de_mapa.get("subtitulo", '') 
    ylabel = propieadades_de_mapa.get("ylabel", '') 
    xlabel = propieadades_de_mapa.get("xlabel", '') 
    grid = propieadades_de_mapa.get("grid", True) 
    obj_mapeable = propieadades_de_mapa.get("obj_mapeable", None) 
    colorbar_label = propieadades_de_mapa.get("colorbar_label", '') 
    minimo = propieadades_de_mapa.get("colorbar_min", 0) 
    maximo = propieadades_de_mapa.get("colorbar_max", 1.5) 
    
    tipo_de_letra = get_tipo_letra() # fontfamily
    tamanio_de_letra = get_tamanio_de_letra()
    title_size = tamanio_de_letra + 4
    xlabelsize = tamanio_de_letra + 2
    ylabelsize = tamanio_de_letra + 2
    yticksize = tamanio_de_letra + 2
    xticksize = tamanio_de_letra + 2
    colorbar_labelsize = tamanio_de_letra + 2
    colorbar_ticksize = tamanio_de_letra + 1
    
    if obj_axes is None:
        raise ValueError("Debes indicar a qué axis se le pondrán las propiedades.")
    
    ## Titulos
    plt.title(titulo, font=tipo_de_letra, fontweight='bold', fontsize=title_size, pad = 10)
    if titulo and subtitulo:
        plt.title(titulo + "\n" + subtitulo, font=tipo_de_letra, fontweight='bold', fontsize=title_size, pad = 20)
    
    # Grid
    plt.grid(grid, which='both', linestyle='--', color='gray', alpha=0.5)
    
    # xlabel y ylabel con tipo y tamaño de letra
    obj_axes.set_xlabel(xlabel, fontname=tipo_de_letra, fontweight='bold', fontsize=xlabelsize)
    obj_axes.set_ylabel(ylabel, fontname=tipo_de_letra, fontweight='bold', fontsize=ylabelsize)
    
    # Ejes: tamaño y tipo de letra de los ticks X y Y
    for label in obj_axes.get_xticklabels():
        label.set_fontname(tipo_de_letra)
        label.set_fontsize(xticksize)
    for label in obj_axes.get_yticklabels():
        label.set_fontname(tipo_de_letra)
        label.set_fontsize(yticksize)
    
    if obj_mapeable is not None:
        cb = plt.colorbar(obj_mapeable, label=colorbar_label, orientation='vertical', pad=0.02, aspect=30, ticks=np.round(np.linspace(minimo, maximo, 7), get_decimales_figuras()))
        cb.set_label(colorbar_label, fontname=tipo_de_letra, fontsize=colorbar_labelsize, fontweight='bold')
        # Ajustar tamaño y tipo de letra de los ticks del colorbar
        for label in cb.ax.get_yticklabels():
            label.set_fontname(tipo_de_letra)
            label.set_fontsize(colorbar_ticksize)
    
    plt.tight_layout()
    
def crear_titulos_de_mapa_y_nombre_de_guardado(tspan: pd.DatetimeIndex, NS_sonda: str) -> dict:
    """
    Descripción:
        Genera el título principal, subtítulo y nombre de archivo para un mapa de trayectorias
        de sonda oceanográfica. Formatea las fechas y combina información del número de serie
        de la sonda con el origen de los datos.

    Parámetros:
        tspan (pd.DatetimeIndex): Índice de fechas que representa el rango temporal de los datos.
            Se utiliza para extraer las fechas inicial y final.
        NS_sonda (str): Número de serie de la sonda oceanográfica (sin el prefijo "NS-").

    Retorna:
        dict: Diccionario con tres elementos:
            - "titulo" (str): Título principal del mapa.
            - "subtitulo" (str): Subtítulo con detalles de la sonda, origen y fechas.
            - "nombre_de_guardado" (str): Nombre de archivo sin espacios ni caracteres especiales.

    Ejemplo:
        >>> import pandas as pd
        >>> tspan = pd.date_range('2025-01-15', '2025-01-25', freq='H')
        >>> NS_sonda = '300534063808640'
        >>> resultado = crear_titulos_de_mapa_y_nombre_de_guardado(tspan, NS_sonda)
        >>> print(resultado["titulo"])
        'MAPA DE TRAYECTORIAS SONDA OCEANOGRÁFICA'
        >>> print(resultado["subtitulo"])
        'NS-300534063808640-IOOS-20250115-20250125'
        >>> print(resultado["nombre_de_guardado"])
        'MAPA_DE_TRAYECTORIAS_SONDA_OCEANOGRAFICANS_300534063808640_IOOS_20250115_20250125'

    Notas:
        - Las fechas se formatean como 'YYYYMMDD'.
        - El origen de los datos se obtiene de la función get_origen_de_los_datos().
        - En el nombre de guardado, los espacios se reemplazan por guiones bajos.
        - Los guiones se reemplazan por guiones bajos en el nombre de guardado.
        - Las letras acentuadas (Á) se normalizan en el nombre de guardado.

    Funciones auxiliares:
        - get_origen_de_los_datos(): Obtiene el origen configurado de los datos

    Categoría:
        Gráficos
    """
    
    origen_de_los_datos = get_origen_de_los_datos()
    t0str = tspan.min().strftime('%Y%m%d')
    tEstr = tspan.max().strftime('%Y%m%d')
    strDeFechas = str(f"{t0str}-{tEstr}")
    titulo = str(f"MAPA DE TRAYECTORIAS SONDA OCEANOGRÁFICA")
    subtitulo = str(f"NS-{NS_sonda}-{origen_de_los_datos}-{strDeFechas}") 
    nombre_de_guardado = (titulo + subtitulo).replace(" ", "_").replace("-", "_").replace("Á", "A")

    output = {
        "titulo": titulo,
        "subtitulo": subtitulo,
        "nombre_de_guardado": nombre_de_guardado
    }

    return output