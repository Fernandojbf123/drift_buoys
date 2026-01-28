import matplotlib.pyplot as plt
from Funciones.Utils.utils_get_config_vars import *
import numpy as np

def dar_formato_a_mapa(propieadades_de_mapa) -> None:
    """
    Docstring for dar_formato_a_mapa
    propieadades_de_mapa = {
        "obj_axes": ax,  # axis de matplotlib
        "titulo": '', str
        "subtitulo":'', str
        "ylabel":'', str
        "xlabel": '', str
        "grid": True, boolean
        "obj_mapeable": None || PathCollection from scatter,
        "colorbar_label": '', str
        "colorbar_min": 0, float
        "colorbar_max": 1.5, float
    }
    ax: es el axis de matplotlib a formatear
    colorbar: es la barra de color a agregar (si aplica)
    """
    
    propieadades_de_mapa_default = {
        "obj_axes": None,  # axis de matplotlib
        "titulo": '', 
        "subtitulo":'', 
        "ylabel":'', 
        "xlabel": '', 
        "grid": True, 
        "obj_mapeable": None, 
        "colorbar_label": '', 
        "colorbar_min": 0, 
        "colorbar_max": 1.5, 
    }
    
    # Extraer propiedades con valores por defecto si no se proporcionan
    obj_axes = propieadades_de_mapa.get("obj_axes", propieadades_de_mapa_default["obj_axes"])
    titulo = propieadades_de_mapa.get("titulo", propieadades_de_mapa_default["titulo"]) 
    subtitulo = propieadades_de_mapa.get("subtitulo", propieadades_de_mapa_default["subtitulo"]) 
    ylabel = propieadades_de_mapa.get("ylabel", propieadades_de_mapa_default["ylabel"]) 
    xlabel = propieadades_de_mapa.get("xlabel", propieadades_de_mapa_default["xlabel"]) 
    grid = propieadades_de_mapa.get("grid", propieadades_de_mapa_default["grid"]) 
    obj_mapeable = propieadades_de_mapa.get("obj_mapeable", propieadades_de_mapa_default["obj_mapeable"]) 
    colorbar_label = propieadades_de_mapa.get("colorbar_label", propieadades_de_mapa_default["colorbar_label"]) 
    minimo = propieadades_de_mapa.get("colorbar_min", propieadades_de_mapa_default["colorbar_min"]) 
    maximo = propieadades_de_mapa.get("colorbar_max", propieadades_de_mapa_default["colorbar_max"]) 
    
    tipo_de_letra = get_tipo_letra() # fontfamily
    tamanio_de_letra = get_tamanio_letra()
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